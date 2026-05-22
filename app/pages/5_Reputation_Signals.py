import streamlit as st

from app.utils import format_percent, get_available_columns, require_processed_data

st.title("Reputation Signals")
df = require_processed_data()

if "review_signal" in df.columns:
    st.subheader("Review Signal Distribution")
    st.bar_chart(df["review_signal"].fillna("Unknown").value_counts())

if "review_sentiment" in df.columns:
    st.subheader("Review Sentiment Distribution")
    st.bar_chart(df["review_sentiment"].fillna("Unknown").value_counts())

if "total_reviews" in df.columns and "positive_ratio" in df.columns:
    st.subheader("Reviews vs Positive Ratio")
    scatter_df = df[["total_reviews", "positive_ratio"]].dropna().copy()
    scatter_df["positive_percent"] = scatter_df["positive_ratio"] * 100
    st.line_chart(scatter_df.sort_values("total_reviews").set_index("total_reviews")["positive_percent"])

if {"Name", "positive_ratio", "total_reviews"}.issubset(df.columns):
    st.subheader("Top Games by Positive Ratio (at least 20 reviews)")
    filtered = df[df["total_reviews"].fillna(0) >= 20].copy()
    top_games = filtered.sort_values(["positive_ratio", "total_reviews"], ascending=[False, False]).head(30)
    top_games["positive_ratio"] = top_games["positive_ratio"].apply(format_percent)
    st.dataframe(top_games[["Name", "positive_ratio", "total_reviews"]], use_container_width=True)
else:
    preview_cols = get_available_columns(df, ["Name", "positive_ratio", "total_reviews"])
    if preview_cols:
        st.dataframe(df[preview_cols].head(30), use_container_width=True)
