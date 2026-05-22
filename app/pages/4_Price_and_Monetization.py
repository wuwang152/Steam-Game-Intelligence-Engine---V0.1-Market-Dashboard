import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "steam_games_cleaned.csv"

df = pd.read_csv(DATA_PATH)
st.title("Price and Monetization")
st.bar_chart(df["price_bucket"].value_counts().sort_index())
st.write(df[["Name", "Price", "Discount", "DLC count", "price_bucket"]].head(200))
