import streamlit as st
from app.utils import require_data_page

df = require_data_page("Genre/Tag Explorer")
if df is not None and "tag_count" in df.columns:
    max_tags = int(df["tag_count"].max()) if not df.empty else 0
    min_tags = st.slider("Minimum tag_count", min_value=0, max_value=max_tags, value=min(3, max_tags))
    subset = df[df["tag_count"].fillna(0) >= min_tags]
    cols = [c for c in ["Name", "Genres", "Tags", "genre_count", "tag_count"] if c in df.columns]
    st.write(subset[cols].head(300))
else:
    st.info("Missing required column: tag_count")
