"""Steam Game Intelligence Engine dashboard home page."""

import streamlit as st
from app.utils import require_data_page

st.set_page_config(page_title="Steam Game Intelligence Engine", layout="wide")

df = require_data_page("Steam Game Intelligence Engine — V0.1")
st.caption("Market dashboard built from cleaned and engineered Steam dataset.")

if df is not None:
    st.metric("Games", f"{len(df):,}")
    st.metric("Median Price", f"${df['Price'].median():.2f}")
    st.metric("Median Positive Ratio", f"{df['positive_ratio'].median():.2%}")
    st.dataframe(df.head(50), use_container_width=True)
