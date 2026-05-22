import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "steam_games_cleaned.csv"

df = pd.read_csv(DATA_PATH)
st.title("Overview")
st.write(df[["Name", "release_year", "Price", "owners_mid", "positive_ratio"]].head(200))
