import streamlit as st

from app.utils import require_processed_data

st.title("Reputation Signals")
df = require_processed_data()
st.scatter_chart(df[["total_reviews", "positive_ratio"]].fillna(0))
st.bar_chart(df["review_sentiment"].value_counts())
st.bar_chart(df["review_signal"].value_counts())
