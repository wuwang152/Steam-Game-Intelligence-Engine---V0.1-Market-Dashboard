import streamlit as st

from app.utils import require_processed_data

st.title("Genre/Tag Explorer")
df = require_processed_data()
min_tags = st.slider("Minimum tag_count", min_value=0, max_value=int(df["tag_count"].max() if not df.empty else 0), value=3)
subset = df[df["tag_count"].fillna(0) >= min_tags]
st.write(subset[["Name", "Genres", "Tags", "genre_count", "tag_count"]].head(300))
