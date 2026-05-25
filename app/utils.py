from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "steam_games_cleaned.csv"


@st.cache_data
def load_processed_data() -> pd.DataFrame | None:
    if not DATA_PATH.exists():
        return None
    return pd.read_csv(DATA_PATH)


def require_processed_data() -> pd.DataFrame:
    df = load_processed_data()
    if df is None:
        st.warning(
            "未找到处理后的数据集。请运行 `python scripts/run_pipeline.py` "
            "生成 `data/processed/steam_games_cleaned.csv`。"
        )
        st.stop()
    return df


def safe_column(df: pd.DataFrame, column_name: str, default=None) -> pd.Series:
    if column_name in df.columns:
        return df[column_name]
    return pd.Series([default] * len(df), index=df.index)


def format_percent(value) -> str:
    if pd.isna(value):
        return "暂无"
    return f"{float(value):.1%}"


DISPLAY_COLUMN_MAP = {
    "AppID": "AppID",
    "Name": "游戏名称",
    "release_year": "发行年份",
    "Price": "价格",
    "price_bucket": "价格分层",
    "owners_mid": "估计拥有者中位数",
    "owners_low": "估计拥有者下界",
    "owners_high": "估计拥有者上界",
    "total_reviews": "评论数",
    "positive_ratio": "好评率",
    "positive_rate": "好评率",
    "review_signal": "评论热度信号",
    "review_sentiment": "口碑情绪",
    "median_owners_mid": "估计拥有者中位数",
    "median_total_reviews": "评论数中位数",
    "median_positive_rate_reviewed": "有评论游戏好评率中位数",
    "count": "数量",
    "share": "占比",
    "supports_simplified_chinese": "是否支持简体中文",
    "supports_english": "是否支持英文",
    "supports_japanese": "是否支持日文",
    "supports_korean": "是否支持韩文",
    "has_chinese_audio": "是否支持中文语音",
    "Genres": "游戏类型",
    "Tags": "标签",
    "Categories": "功能分类",
    "Developers": "开发商",
    "Publishers": "发行商",
    "heuristic_reason": "启发式原因",
    "Discount": "折扣",
    "DLC count": "DLC 数量",
    "genre_count": "类型数量",
    "tag_count": "标签数量",
    "platform_count": "平台数量",
}

PRICE_BUCKET_LABELS = {"free": "免费", "budget": "低价", "mid": "中价", "premium": "高价", "luxury": "豪华价位"}
REVIEW_SIGNAL_LABELS = {"no_signal": "无评论信号", "very_low": "极低", "low": "较低", "medium": "中等", "high": "较高"}
REVIEW_SENTIMENT_LABELS = {"no_reviews": "无评论", "weak": "较弱", "mixed": "一般", "strong": "较强"}
LANGUAGE_LABELS = {"simplified_chinese": "简体中文", "english": "英文", "japanese": "日文", "korean": "韩文", "chinese_audio": "中文语音"}
HEURISTIC_REASON_LABELS = {
    "high_rating_low_estimated_ownership": "高口碑低估计拥有者",
    "low_price_high_rating": "低价高口碑",
    "high_attention_low_rating": "高关注低口碑",
    "chinese_supported_high_rating_low_exposure": "已支持简中的高口碑低曝光候选",
    "missing_simplified_chinese_high_rating_attention": "未支持简中的高口碑高关注候选",
}
BOOLEAN_LABELS = {True: "是", False: "否"}


def rename_display_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=DISPLAY_COLUMN_MAP)


def map_display_value(value, mapping: dict[str, str]) -> str:
    if pd.isna(value):
        return "未知"
    key = str(value)
    return mapping.get(key, key)


def map_display_series(series: pd.Series, mapping: dict[str, str]) -> pd.Series:
    return series.map(lambda x: map_display_value(x, mapping))


def format_percent_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").map(lambda x: f"{x:.1%}" if pd.notna(x) else "—")
    return out


def format_count_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").map(lambda x: f"{x:,.0f}" if pd.notna(x) else "—")
    return out


def format_boolean_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            normalized = out[col].map(
                lambda x: True if (isinstance(x, str) and x.lower() in {"true", "1", "yes"}) or x is True or x == 1 else False if (isinstance(x, str) and x.lower() in {"false", "0", "no"}) or x is False or x == 0 else pd.NA
            )
            out[col] = normalized.map(lambda x: BOOLEAN_LABELS[x] if x in BOOLEAN_LABELS else "—")
    return out


def format_ranking_table_for_display(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col, mp in {
        "price_bucket": PRICE_BUCKET_LABELS,
        "review_signal": REVIEW_SIGNAL_LABELS,
        "review_sentiment": REVIEW_SENTIMENT_LABELS,
        "language": LANGUAGE_LABELS,
        "heuristic_reason": HEURISTIC_REASON_LABELS,
    }.items():
        if col in out.columns:
            out[col] = map_display_series(out[col], mp)
    if "release_year" in out.columns:
        out["release_year"] = pd.to_numeric(out["release_year"], errors="coerce").map(
            lambda x: str(int(x)) if pd.notna(x) else "—"
        )
    if "AppID" in out.columns:
        out["AppID"] = pd.to_numeric(out["AppID"], errors="coerce").map(
            lambda x: str(int(x)) if pd.notna(x) else "—"
        )
    out = format_percent_columns(out, ["positive_rate", "positive_ratio", "share", "median_positive_rate_reviewed"])
    out = format_count_columns(out, ["owners_mid", "owners_low", "owners_high", "total_reviews", "count", "median_owners_mid", "median_total_reviews"])
    out = format_boolean_columns(out, ["supports_simplified_chinese", "supports_english", "supports_japanese", "supports_korean", "has_chinese_audio"])
    return rename_display_columns(out)


def get_available_columns(df: pd.DataFrame, columns: list[str]) -> list[str]:
    return [col for col in columns if col in df.columns]


def top_split_values(df: pd.DataFrame, column: str, sep: str = ";", top_n: int = 20) -> pd.Series:
    if column not in df.columns:
        return pd.Series(dtype="int64")

    raw = df[column].dropna().astype(str)
    normalized = raw.str.replace(",", sep, regex=False) if sep != "," else raw.str.replace(";", sep, regex=False)
    split_values = normalized.str.split(sep).explode().str.strip()
    clean_values = split_values[split_values != ""]
    return clean_values.value_counts().head(top_n)


@st.cache_data(show_spinner=False)
def top_split_values_cached(series: pd.Series, sep: str = ";", top_n: int = 20) -> pd.Series:
    raw = series.dropna().astype(str)
    normalized = raw.str.replace(",", sep, regex=False) if sep != "," else raw.str.replace(";", sep, regex=False)
    split_values = normalized.str.split(sep).explode().str.strip()
    clean_values = split_values[split_values != ""]
    return clean_values.value_counts().head(top_n)
