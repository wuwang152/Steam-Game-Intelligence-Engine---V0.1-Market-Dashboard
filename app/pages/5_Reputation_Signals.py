import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "steam_games_cleaned.csv"

df = pd.read_csv(DATA_PATH)
st.title("Reputation Signals")
st.scatter_chart(df[["total_reviews", "positive_ratio"]].fillna(0))
st.bar_chart(df["review_signal"].value_counts())
