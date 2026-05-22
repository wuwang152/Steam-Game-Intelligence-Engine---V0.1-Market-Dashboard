import streamlit as st
from app.utils import require_data_page

df = require_data_page("Price and Monetization")
if df is not None and "price_bucket" in df.columns:
    st.bar_chart(df["price_bucket"].value_counts().sort_index())
    cols = [c for c in ["Name", "Price", "Discount", "DLC count", "price_bucket"] if c in df.columns]
    st.write(df[cols].head(200))
else:
    st.info("Missing required column: price_bucket")
