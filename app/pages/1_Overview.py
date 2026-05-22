import streamlit as st
from app.utils import require_data_page

df = require_data_page("Overview")
if df is not None:
    cols = [c for c in ["Name", "release_year", "Price", "owners_mid", "positive_ratio"] if c in df.columns]
    st.write(df[cols].head(200))
