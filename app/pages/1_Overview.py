import streamlit as st

from app.utils import require_processed_data

st.title("Overview")
df = require_processed_data()
st.write(df[["Name", "release_year", "Price", "owners_mid", "positive_ratio"]].head(200))
