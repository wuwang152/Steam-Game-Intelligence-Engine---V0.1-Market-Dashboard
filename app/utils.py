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
