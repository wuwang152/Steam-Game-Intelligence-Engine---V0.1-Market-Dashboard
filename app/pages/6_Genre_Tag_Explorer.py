import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "steam_games_cleaned.csv"

df = pd.read_csv(DATA_PATH)
st.title("Genre/Tag Explorer")
min_tags = st.slider("Minimum tag_count", min_value=0, max_value=int(df["tag_count"].max() if not df.empty else 0), value=3)
subset = df[df["tag_count"].fillna(0) >= min_tags]
st.write(subset[["Name", "Genres", "Tags", "genre_count", "tag_count"]].head(300))
