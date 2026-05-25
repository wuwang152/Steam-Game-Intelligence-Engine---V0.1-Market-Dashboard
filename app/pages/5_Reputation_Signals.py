import pandas as pd
import streamlit as st

from app.utils import REVIEW_SENTIMENT_LABELS, REVIEW_SIGNAL_LABELS, format_percent, get_available_columns, map_display_series, rename_display_columns, require_processed_data

REVIEW_SIGNAL_ORDER = ["no_signal", "very_low", "low", "medium", "high"]
REVIEW_SENTIMENT_ORDER = ["no_reviews", "weak", "mixed", "strong"]

st.title("口碑信号")
df = require_processed_data()

if "review_signal" in df.columns:
    st.subheader("评论热度信号分布")
    signal_series = map_display_series(df["review_signal"], REVIEW_SIGNAL_LABELS)
    order = [x for x in REVIEW_SIGNAL_ORDER if x in signal_series.unique()]
    remainder = sorted([x for x in signal_series.unique() if x not in order])
    st.bar_chart(signal_series.value_counts().reindex(order + remainder, fill_value=0))

if "review_sentiment" in df.columns:
    st.subheader("口碑情绪分布")
    sentiment_series = map_display_series(df["review_sentiment"], REVIEW_SENTIMENT_LABELS)
    order = [x for x in REVIEW_SENTIMENT_ORDER if x in sentiment_series.unique()]
    remainder = sorted([x for x in sentiment_series.unique() if x not in order])
    st.bar_chart(sentiment_series.value_counts().reindex(order + remainder, fill_value=0))

if "total_reviews" in df.columns and "positive_ratio" in df.columns:
    st.subheader("评论数与好评率")
    st.caption("按评论数分桶展示中位好评率，更轻量且更易解释。")
    scatter_df = df[["total_reviews", "positive_ratio"]].dropna().copy()
    bins = [20, 100, 500, 1_000, 5_000, 10_000, 50_000, float("inf")]
    labels = ["20–100", "100–500", "500–1k", "1k–5k", "5k–10k", "10k–50k", "50k+"]
    scatter_df = scatter_df[scatter_df["total_reviews"] >= 20]
    scatter_df["评论数分桶"] = pd.cut(scatter_df["total_reviews"], bins=bins, labels=labels, right=False, include_lowest=True)
    bucket_median = (
        scatter_df.groupby("评论数分桶", observed=False)["positive_ratio"]
        .median()
        .mul(100)
        .rename("中位好评率（%）")
    )
    st.bar_chart(bucket_median.dropna(), x_label="评论数分桶", y_label="中位好评率（%）")

if {"Name", "positive_ratio", "total_reviews"}.issubset(df.columns):
    st.subheader("按好评率排序的热门游戏（至少 20 条评论）")
    filtered = df[df["total_reviews"].fillna(0) >= 20].copy()
    top_games = filtered.sort_values(["positive_ratio", "total_reviews"], ascending=[False, False]).head(30)
    top_games["positive_ratio"] = top_games["positive_ratio"].apply(format_percent)
    st.dataframe(rename_display_columns(top_games[["Name", "positive_ratio", "total_reviews"]]), use_container_width=True)
else:
    preview_cols = get_available_columns(df, ["Name", "positive_ratio", "total_reviews"])
    if preview_cols:
        st.dataframe(rename_display_columns(df[preview_cols].head(30)), use_container_width=True)
