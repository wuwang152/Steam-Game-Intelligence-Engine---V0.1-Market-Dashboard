import streamlit as st

from app.utils import format_percent, get_available_columns, require_processed_data

REVIEW_SIGNAL_ORDER = ["no_signal", "very_low", "low", "medium", "high"]
REVIEW_SENTIMENT_ORDER = ["no_reviews", "weak", "mixed", "strong"]

st.title("Reputation Signals")
df = require_processed_data()

if "review_signal" in df.columns:
    st.subheader("Review Signal Distribution")
    signal_series = df["review_signal"].fillna("Unknown").astype(str)
    order = [x for x in REVIEW_SIGNAL_ORDER if x in signal_series.unique()]
    remainder = sorted([x for x in signal_series.unique() if x not in order])
    st.bar_chart(signal_series.value_counts().reindex(order + remainder, fill_value=0))

if "review_sentiment" in df.columns:
    st.subheader("Review Sentiment Distribution")
    sentiment_series = df["review_sentiment"].fillna("Unknown").astype(str)
    order = [x for x in REVIEW_SENTIMENT_ORDER if x in sentiment_series.unique()]
    remainder = sorted([x for x in sentiment_series.unique() if x not in order])
    st.bar_chart(sentiment_series.value_counts().reindex(order + remainder, fill_value=0))

if "total_reviews" in df.columns and "positive_ratio" in df.columns:
    st.subheader("Total Reviews vs Positive Rate")
    st.caption("Positive Rate is most meaningful for games with reviews.")
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
