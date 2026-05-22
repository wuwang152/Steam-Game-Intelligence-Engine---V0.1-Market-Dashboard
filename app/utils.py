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
            "Processed dataset is missing. Run `python scripts/run_pipeline.py` "
            "to generate `data/processed/steam_games_cleaned.csv`."
        )
        st.stop()
    return df


def safe_column(df: pd.DataFrame, column_name: str, default=None) -> pd.Series:
    if column_name in df.columns:
        return df[column_name]
    return pd.Series([default] * len(df), index=df.index)


def format_percent(value) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.1%}"


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
