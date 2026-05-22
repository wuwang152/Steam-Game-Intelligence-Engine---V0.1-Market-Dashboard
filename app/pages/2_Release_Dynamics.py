import streamlit as st
from app.utils import require_data_page

df = require_data_page("Release Dynamics")
if df is not None and "release_year" in df.columns:
    release_counts = df.groupby("release_year", dropna=True).size().reset_index(name="games")
    st.line_chart(release_counts.set_index("release_year"))
else:
    st.info("Missing required column: release_year")
