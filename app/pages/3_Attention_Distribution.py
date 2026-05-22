import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "steam_games_cleaned.csv"

df = pd.read_csv(DATA_PATH)
st.title("Attention Distribution")
st.bar_chart(df["Peak CCU"].fillna(0).clip(upper=df["Peak CCU"].quantile(0.99)))
