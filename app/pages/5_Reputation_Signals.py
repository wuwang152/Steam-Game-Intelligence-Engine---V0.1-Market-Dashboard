import streamlit as st
from app.utils import require_data_page

df = require_data_page("Reputation Signals")
if df is not None and {"total_reviews", "positive_ratio", "review_signal", "review_sentiment"}.issubset(df.columns):
    st.scatter_chart(df[["total_reviews", "positive_ratio"]].fillna(0))
    st.subheader("Review Signal (volume)")
    st.bar_chart(df["review_signal"].value_counts())
    st.subheader("Review Sentiment (ratio)")
    st.bar_chart(df["review_sentiment"].value_counts())
else:
    st.info("Missing required review columns")
