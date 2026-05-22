import streamlit as st

from app.utils import get_available_columns, require_processed_data

st.title("Price and Monetization")
df = require_processed_data()

if "price_bucket" in df.columns:
    st.subheader("Price Bucket Distribution")
    st.bar_chart(df["price_bucket"].fillna("Unknown").value_counts())

if "Price" in df.columns:
    st.subheader("Free vs Paid Share")
    free_paid = df["Price"].fillna(0).apply(lambda x: "Free" if x == 0 else "Paid").value_counts()
    st.bar_chart(free_paid)

if "price_bucket" in df.columns and "total_reviews" in df.columns:
    st.subheader("Median Total Reviews by Price Bucket")
    median_reviews = df.groupby("price_bucket", dropna=True)["total_reviews"].median().sort_index()
    st.bar_chart(median_reviews)

st.subheader("Price and Monetization Table")
table_cols = get_available_columns(df, ["Name", "Price", "Discount", "DLC count", "price_bucket"])
if table_cols:
    st.dataframe(df[table_cols].head(250), use_container_width=True)
else:
    st.info("No price or monetization table columns are available.")
