import streamlit as st

from app.utils import get_available_columns, require_processed_data

st.title("Attention Distribution")
df = require_processed_data()

c1, c2, c3 = st.columns(3)
if "total_reviews" in df.columns:
    c1.metric("Median Total Reviews", f"{df['total_reviews'].median():,.0f}")
    c2.metric("Max Total Reviews", f"{df['total_reviews'].max():,.0f}")
else:
    c1.metric("Median Total Reviews", "N/A")
    c2.metric("Max Total Reviews", "N/A")

if "Peak CCU" in df.columns:
    c3.metric("Median Peak CCU", f"{df['Peak CCU'].median():,.0f}")
else:
    c3.metric("Median Peak CCU", "N/A")

if "review_signal" in df.columns:
    st.subheader("Review Signal Distribution")
    review_signal_counts = df["review_signal"].fillna("Unknown").value_counts()
    st.bar_chart(review_signal_counts)

if "Name" in df.columns and "total_reviews" in df.columns:
    st.subheader("Top 20 Games by Total Reviews")
    top_reviews = df[["Name", "total_reviews"]].dropna().sort_values("total_reviews", ascending=False).head(20)
    st.dataframe(top_reviews, use_container_width=True)
else:
    cols = get_available_columns(df, ["Name", "total_reviews"])
    if cols:
        st.dataframe(df[cols].head(20), use_container_width=True)
