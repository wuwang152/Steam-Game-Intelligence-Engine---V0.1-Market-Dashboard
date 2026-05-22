import streamlit as st

from app.utils import require_processed_data

st.title("Release Dynamics")
df = require_processed_data()
release_counts = df.groupby("release_year", dropna=True).size().reset_index(name="games")
st.line_chart(release_counts.set_index("release_year"))
