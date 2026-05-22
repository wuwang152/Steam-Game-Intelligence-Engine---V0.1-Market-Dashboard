"""Steam Game Intelligence Engine dashboard home page."""

import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "steam_games_cleaned.csv"

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)

st.set_page_config(page_title="Steam Game Intelligence Engine", layout="wide")
st.title("Steam Game Intelligence Engine — V0.1")
st.caption("Market dashboard built from cleaned and engineered Steam dataset.")

df = load_data()
st.metric("Games", f"{len(df):,}")
st.metric("Median Price", f"${df['Price'].median():.2f}")
st.metric("Median Positive Ratio", f"{df['positive_ratio'].median():.2%}")

st.dataframe(df.head(50), use_container_width=True)
