import pandas as pd
import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import (
    REVIEW_SIGNAL_LABELS,
    format_ranking_table_for_display,
    get_available_columns,
    map_display_series,
    rename_display_columns,
    require_processed_data,
)

REVIEW_SIGNAL_ORDER = ["no_signal", "very_low", "low", "medium", "high"]
GEN_CMD = (
    "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv "
    "--output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
)


def _backend_table_warning() -> None:
    st.warning("未检测到对应的后端聚合表。请先运行 generate_dashboard_tables.py 生成后端聚合表。")
    st.code(GEN_CMD)


st.title("关注度分布")
df = require_processed_data()

c1, c2, c3 = st.columns(3)
if "total_reviews" in df.columns:
    c1.metric("评论数中位数", f"{df['total_reviews'].median():,.0f}")
    c2.metric("评论数最大值", f"{df['total_reviews'].max():,.0f}")
else:
    c1.metric("评论数中位数", "N/A")
    c2.metric("评论数最大值", "N/A")

if "Peak CCU" in df.columns:
    c3.metric("峰值 CCU 中位数", f"{df['Peak CCU'].median():,.0f}")
else:
    c3.metric("峰值 CCU 中位数", "N/A")

st.subheader("评论热度信号分布")
review_signal_table = load_dashboard_table("review_signal_distribution")
if review_signal_table is not None and not review_signal_table.empty and {"review_signal", "count"}.issubset(review_signal_table.columns):
    st.caption("全量样本后端聚合结果")
    chart_df = review_signal_table.copy()
    chart_df["review_signal_display"] = map_display_series(chart_df["review_signal"], REVIEW_SIGNAL_LABELS)
    ordered = [x for x in REVIEW_SIGNAL_ORDER if x in chart_df["review_signal"].astype(str).tolist()]
    order_map = {k: i for i, k in enumerate(ordered)}
    chart_df = chart_df.sort_values(by="review_signal", key=lambda s: s.map(lambda x: order_map.get(str(x), 999)))
    st.bar_chart(chart_df.set_index("review_signal_display")["count"])

    preview_cols = [
        "review_signal",
        "count",
        "share",
        "median_owners_mid",
        "median_positive_rate_reviewed",
    ]
    preview = review_signal_table[[c for c in preview_cols if c in review_signal_table.columns]].copy()
    preview["review_signal"] = map_display_series(preview["review_signal"], REVIEW_SIGNAL_LABELS)
    st.dataframe(format_ranking_table_for_display(preview), use_container_width=True)
    st.caption("评论热度信号优先读取后端聚合表 review_signal_distribution.csv，反映全量样本的评论关注度结构。")
else:
    _backend_table_warning()
    st.caption("当前筛选样本结果")
    if "review_signal" in df.columns:
        signal_series = map_display_series(df["review_signal"], REVIEW_SIGNAL_LABELS)
        ordered = [x for x in REVIEW_SIGNAL_ORDER if x in signal_series.unique()]
        remainder = sorted([x for x in signal_series.unique() if x not in ordered])
        review_signal_counts = signal_series.value_counts().reindex(ordered + remainder, fill_value=0)
        st.bar_chart(review_signal_counts)

if "Name" in df.columns and "total_reviews" in df.columns:
    st.subheader("评论数 Top 20 游戏")
    top_reviews_table = load_dashboard_table("top_games_by_reviews")
    if top_reviews_table is not None and not top_reviews_table.empty:
        st.caption("全量样本后端聚合结果")
        display_cols = [
            "Name",
            "release_year",
            "price_bucket",
            "owners_mid",
            "total_reviews",
            "positive_rate",
            "supports_simplified_chinese",
            "Genres",
            "Tags",
        ]
        display_df = top_reviews_table[[c for c in display_cols if c in top_reviews_table.columns]].copy()
        st.dataframe(format_ranking_table_for_display(display_df), use_container_width=True)
        st.caption("热门评论榜基于后端榜单表 top_games_by_reviews.csv，仅用于描述评论关注度，不代表个性化推荐。")
    else:
        _backend_table_warning()
        st.caption("当前筛选样本结果")
        top_reviews = df[["Name", "total_reviews"]].dropna().sort_values("total_reviews", ascending=False).head(20)
        st.dataframe(rename_display_columns(top_reviews), use_container_width=True)
else:
    cols = get_available_columns(df, ["Name", "total_reviews"])
    if cols:
        st.dataframe(rename_display_columns(df[cols].head(20)), use_container_width=True)
