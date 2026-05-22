import streamlit as st

from app.utils import require_processed_data

st.title("Price and Monetization")
df = require_processed_data()
st.bar_chart(df["price_bucket"].value_counts().sort_index())
st.write(df[["Name", "Price", "Discount", "DLC count", "price_bucket"]].head(200))
