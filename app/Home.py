"""Steam Game Intelligence Engine dashboard home page."""

from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from app.utils import (
    REVIEW_SENTIMENT_LABELS,
    REVIEW_SIGNAL_LABELS,
    load_processed_data,
    map_display_series,
    rename_display_columns,
    top_split_values,
)

st.set_page_config(page_title="Steam 游戏智能分析看板", layout="wide")


PREVIEW_COLUMNS = [
    "Name",
    "release_year",
    "Price",
    "owners_mid",
    "total_reviews",
    "positive_ratio",
    "review_signal",
    "review_sentiment",
    "Genres",
    "Tags",
]
MAX_SCATTER_POINTS = 5000
SCATTER_RANDOM_STATE = 42


def _to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _resolve_column(df: pd.DataFrame, aliases: list[str]) -> str | None:
    for alias in aliases:
        if alias in df.columns:
            return alias
    return None


def _resolve_platform_columns(df: pd.DataFrame) -> dict[str, str]:
    candidates = {
        "Windows": ["Windows", "windows"],
        "Mac": ["Mac", "mac"],
        "Linux": ["Linux", "linux"],
    }
    resolved: dict[str, str] = {}
    for label, names in candidates.items():
        for name in names:
            if name in df.columns:
                resolved[label] = name
                break
    return resolved


def _apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("筛选")
    filtered = df.copy()

    release_year_col = _resolve_column(filtered, ["release_year", "Release Year"])
    price_col = _resolve_column(filtered, ["Price", "price"])
    genre_col = _resolve_column(filtered, ["Genres", "genres"])
    positive_col = _resolve_column(filtered, ["positive", "Positive"])

    if release_year_col and filtered[release_year_col].notna().any():
        years = _to_numeric(filtered[release_year_col])
        year_min = int(years.min())
        year_max = int(years.max())
        selected_years = st.sidebar.slider("发行年份", year_min, year_max, (year_min, year_max))
        filtered = filtered[years.between(selected_years[0], selected_years[1], inclusive="both")]

    if price_col and filtered[price_col].notna().any():
        prices = _to_numeric(filtered[price_col]).fillna(0)
        price_min = float(prices.min())
        price_max = float(prices.max())
        selected_price = st.sidebar.slider(
            "价格区间（美元）",
            min_value=price_min,
            max_value=price_max,
            value=(price_min, price_max),
            step=0.5,
        )
        filtered = filtered[prices.between(selected_price[0], selected_price[1], inclusive="both")]

    platform_cols = _resolve_platform_columns(filtered)
    if platform_cols:
        selected_platforms = st.sidebar.multiselect(
            "平台支持",
            options=list(platform_cols.keys()),
            default=list(platform_cols.keys()),
        )
        if selected_platforms:
            mask = pd.Series(False, index=filtered.index)
            for platform in selected_platforms:
                col = platform_cols[platform]
                values = filtered[col]
                if pd.api.types.is_bool_dtype(values):
                    platform_mask = values.fillna(False)
                else:
                    platform_mask = values.astype(str).str.lower().isin(["true", "1", "yes"])
                mask = mask | platform_mask
            filtered = filtered[mask]

    if genre_col:
        genre_counts = top_split_values(filtered, genre_col, sep=";", top_n=200)
        genre_options = genre_counts.index.tolist()
        selected_genres = st.sidebar.multiselect("游戏类型", options=genre_options)
        if selected_genres:
            genre_pattern = "|".join(selected_genres)
            genre_series = filtered[genre_col].fillna("").astype(str)
            filtered = filtered[genre_series.str.contains(genre_pattern, case=False, regex=True)]

    if positive_col and filtered[positive_col].notna().any():
        positives = _to_numeric(filtered[positive_col]).fillna(0)
        min_positive = int(positives.min())
        max_positive = int(positives.max())
        selected_min_positive = st.sidebar.slider(
            "最低好评数",
            min_value=min_positive,
            max_value=max_positive,
            value=min_positive,
        )
        filtered = filtered[positives >= selected_min_positive]

    return filtered


def _show_kpis(df: pd.DataFrame) -> None:
    st.subheader("核心指标")
    k1, k2, k3 = st.columns(3)
    k4, k5, k6 = st.columns(3)

    price_col = _resolve_column(df, ["Price", "price"])
    owners_col = _resolve_column(df, ["owners_mid", "Owners Mid"])
    peak_ccu_col = _resolve_column(df, ["peak_ccu", "Peak CCU", "Peak_CCU"])
    positive_col = _resolve_column(df, ["positive", "Positive"])
    release_year_col = _resolve_column(df, ["release_year", "Release Year"])

    k1.metric("游戏总数", f"{len(df):,}")

    if price_col and df[price_col].notna().any():
        k2.metric("价格中位数", f"${_to_numeric(df[price_col]).median():.2f}")
    else:
        k2.metric("价格中位数", "暂无")

    if owners_col and df[owners_col].notna().any():
        k3.metric("估计拥有者数量中位数", f"{int(_to_numeric(df[owners_col]).median()):,}")
    else:
        k3.metric("估计拥有者数量中位数", "暂无")

    if peak_ccu_col and df[peak_ccu_col].notna().any():
        k4.metric("平均峰值 CCU", f"{_to_numeric(df[peak_ccu_col]).mean():,.0f}")
    else:
        k4.metric("平均峰值 CCU", "暂无")

    if positive_col and df[positive_col].notna().any():
        k5.metric("平均好评数", f"{_to_numeric(df[positive_col]).mean():,.0f}")
    else:
        k5.metric("平均好评数", "暂无")

    if release_year_col and df[release_year_col].notna().any():
        years = _to_numeric(df[release_year_col])
        k6.metric("发行年份范围", f"{int(years.min())}–{int(years.max())}")
    else:
        k6.metric("发行年份范围", "暂无")


def _show_charts(df: pd.DataFrame) -> None:
    st.subheader("市场分布探索")
    c1, c2 = st.columns(2)

    release_year_col = _resolve_column(df, ["release_year", "Release Year"])
    price_col = _resolve_column(df, ["Price", "price"])
    genre_col = _resolve_column(df, ["Genres", "genres"])
    owners_col = _resolve_column(df, ["owners_mid", "Owners Mid"])
    positive_col = _resolve_column(df, ["positive", "Positive"])

    if release_year_col and df[release_year_col].notna().any():
        by_year = _to_numeric(df[release_year_col]).dropna().astype(int).value_counts().sort_index()
        c1.bar_chart(by_year, x_label="发行年份", y_label="游戏数量")
    else:
        c1.info("缺少发行年份列，无法绘制年度发布图。")

    if price_col and df[price_col].notna().any():
        price_data = _to_numeric(df[price_col]).dropna()
        if not price_data.empty:
            bins = [-0.01, 0.01, 5, 10, 20, 50, float("inf")]
            labels = ["$0", "$0–5", "$5–10", "$10–20", "$20–50", "$50+"]
            bucketed = pd.cut(price_data, bins=bins, labels=labels, include_lowest=True, right=True)
            counts = bucketed.value_counts(sort=False)
            c2.bar_chart(counts, x_label="价格分层", y_label="游戏数量")
        else:
            c2.info("缺少价格列，无法绘制价格分布图。")
    else:
        c2.info("缺少价格列，无法绘制价格分布图。")

    c3, c4 = st.columns(2)
    if genre_col:
        top_genres = top_split_values(df, genre_col, sep=";", top_n=10)
        c3.bar_chart(top_genres, x_label="游戏类型", y_label="游戏数量")
    else:
        c3.info("缺少游戏类型列，无法绘制热门类型图。")

    if owners_col and positive_col:
        scatter_df = df[[owners_col, positive_col]].copy()
        scatter_df[owners_col] = _to_numeric(scatter_df[owners_col])
        scatter_df[positive_col] = _to_numeric(scatter_df[positive_col])
        scatter_df = scatter_df.dropna()
        if not scatter_df.empty:
            if len(scatter_df) > MAX_SCATTER_POINTS:
                scatter_df = scatter_df.sample(n=MAX_SCATTER_POINTS, random_state=SCATTER_RANDOM_STATE)
            scatter_df = scatter_df.rename(columns={owners_col: "拥有者中位估计", positive_col: "好评数"})
            c4.scatter_chart(scatter_df, x="拥有者中位估计", y="好评数")
            c4.caption("为提升渲染速度，散点图默认展示抽样结果。")
        else:
            c4.info("拥有者/好评列存在，但无可绘制数据。")
    else:
        c4.info("散点图需要 owners_mid 与 positive 列。")


def _show_table(df: pd.DataFrame) -> None:
    st.subheader("筛选结果")
    available_preview_cols = [column for column in PREVIEW_COLUMNS if column in df.columns]
    preview_df = df[available_preview_cols].copy() if available_preview_cols else df.copy()
    if "review_signal" in preview_df.columns:
        preview_df["review_signal"] = map_display_series(preview_df["review_signal"], REVIEW_SIGNAL_LABELS)
    if "review_sentiment" in preview_df.columns:
        preview_df["review_sentiment"] = map_display_series(preview_df["review_sentiment"], REVIEW_SENTIMENT_LABELS)
    preview_rows = min(len(preview_df), 500)
    st.caption(f"显示前 {preview_rows:,} 行，共筛选出 {len(df):,} 款游戏")
    st.dataframe(rename_display_columns(preview_df.head(500)), use_container_width=True, hide_index=True)

    csv_buffer = io.StringIO()
    preview_df.to_csv(csv_buffer, index=False)
    st.download_button(
        "下载筛选结果 CSV",
        data=csv_buffer.getvalue(),
        file_name="steam_games_filtered.csv",
        mime="text/csv",
    )


def main() -> None:
    st.title("Steam 游戏智能分析看板 — V0.2")
    st.caption(
        "V0.2 包含分析特征工程、市场洞察与可复现报告生成功能。"
    )
    st.write(
        "可按发行时间、价格、平台、类型与评论热度筛选游戏，快速识别市场模式。"
    )

    df = load_processed_data()
    if df is None:
        st.warning(
            "未在 `data/processed/steam_games_cleaned.csv` 找到处理后数据。"
            "Run `PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv "
            "--output data/processed/steam_games_cleaned.csv` 后再使用此看板。"
        )
        st.stop()

    filtered_df = _apply_filters(df)
    _show_kpis(filtered_df)
    _show_charts(filtered_df)
    _show_table(filtered_df)


main()
