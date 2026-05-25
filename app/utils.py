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
    "Name": "游戏名称",
    "release_year": "发行年份",
    "Price": "价格",
    "price_bucket": "价格分层",
    "owners_mid": "估计拥有者数量（中位）",
    "total_reviews": "评论数",
    "positive_ratio": "好评率",
    "positive_rate": "好评率",
    "review_signal": "评论热度信号",
    "review_sentiment": "口碑情绪",
    "Genres": "游戏类型",
    "Tags": "标签",
    "Discount": "折扣",
    "DLC count": "DLC 数量",
    "genre_count": "类型数量",
    "tag_count": "标签数量",
    "platform_count": "平台数量",
}

PRICE_BUCKET_LABELS = {
    "free": "免费",
    "budget": "低价",
    "mid": "中价",
    "premium": "高价",
    "luxury": "豪华价位",
}

REVIEW_SIGNAL_LABELS = {
    "no_signal": "无信号",
    "very_low": "极低",
    "low": "较低",
    "medium": "中等",
    "high": "较高",
}

REVIEW_SENTIMENT_LABELS = {
    "no_reviews": "无评论",
    "weak": "较弱",
    "mixed": "一般",
    "strong": "较强",
}


def rename_display_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=DISPLAY_COLUMN_MAP)


def map_display_value(value, mapping: dict[str, str]) -> str:
    if pd.isna(value):
        return "未知"
    key = str(value)
    return mapping.get(key, key)


def map_display_series(series: pd.Series, mapping: dict[str, str]) -> pd.Series:
    return series.map(lambda x: map_display_value(x, mapping))


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
