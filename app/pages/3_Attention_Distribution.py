import streamlit as st

from app.utils import get_available_columns, rename_display_columns, require_processed_data

REVIEW_SIGNAL_ORDER = ["no_signal", "very_low", "low", "medium", "high"]

st.title("关注度分布")
df = require_processed_data()

c1, c2, c3 = st.columns(3)
if "total_reviews" in df.columns:
    c1.metric("评论数中位数", f"{df['total_reviews'].median():,.0f}")
    c2.metric("评论数最大值", f"{df['total_reviews'].max():,.0f}")
else:
    c1.metric("评论数中位数", "N/A")
    c2.metric("评论数最大值", "N/A")

if "Peak CCU" in df.columns:
    c3.metric("峰值 CCU 中位数", f"{df['Peak CCU'].median():,.0f}")
else:
    c3.metric("峰值 CCU 中位数", "N/A")

if "review_signal" in df.columns:
    st.subheader("评论热度信号分布")
    signal_series = df["review_signal"].fillna("未知").astype(str)
    ordered = [x for x in REVIEW_SIGNAL_ORDER if x in signal_series.unique()]
    remainder = sorted([x for x in signal_series.unique() if x not in ordered])
    review_signal_counts = signal_series.value_counts().reindex(ordered + remainder, fill_value=0)
    st.bar_chart(review_signal_counts)

if "Name" in df.columns and "total_reviews" in df.columns:
    st.subheader("评论数 Top 20 游戏")
    top_reviews = df[["Name", "total_reviews"]].dropna().sort_values("total_reviews", ascending=False).head(20)
    st.dataframe(rename_display_columns(top_reviews), use_container_width=True)
else:
    cols = get_available_columns(df, ["Name", "total_reviews"])
    if cols:
        st.dataframe(rename_display_columns(df[cols].head(20)), use_container_width=True)
