"""Shared Streamlit helpers for loading data safely."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

PRIMARY = Path(__file__).resolve().parents[1] / "data" / "processed" / "steam_games_cleaned.csv"
SAMPLE = Path(__file__).resolve().parents[1] / "data" / "processed" / "steam_games_cleaned_sample.csv"


def load_dashboard_data() -> pd.DataFrame | None:
    for path in (PRIMARY, SAMPLE):
        if path.exists():
            return pd.read_csv(path)
    return None


def require_data_page(title: str) -> pd.DataFrame | None:
    st.title(title)
    df = load_dashboard_data()
    if df is None:
        st.warning(
            "No cleaned dataset found. Expected either data/processed/steam_games_cleaned.csv "
            "or data/processed/steam_games_cleaned_sample.csv. Run the pipeline first."
        )
        return None
    return df
