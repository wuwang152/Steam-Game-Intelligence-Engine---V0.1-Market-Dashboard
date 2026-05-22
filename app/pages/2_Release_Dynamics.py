import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "steam_games_cleaned.csv"

df = pd.read_csv(DATA_PATH)
st.title("Release Dynamics")
release_counts = df.groupby("release_year", dropna=True).size().reset_index(name="games")
st.line_chart(release_counts.set_index("release_year"))
