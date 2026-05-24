import streamlit as st
import pandas as pd

from app.utils import get_available_columns, require_processed_data

PRICE_BUCKET_ORDER = ["free", "budget", "mid", "premium", "luxury"]

st.title("Overview")
df = require_processed_data()
filtered_df = df.copy()

st.sidebar.header("Overview Filters")
if "release_year" in filtered_df.columns and filtered_df["release_year"].notna().any():
    year_min = int(filtered_df["release_year"].min())
    year_max = int(filtered_df["release_year"].max())
    year_range = st.sidebar.slider("Release year", min_value=year_min, max_value=year_max, value=(year_min, year_max))
    filtered_df = filtered_df[filtered_df["release_year"].between(year_range[0], year_range[1], inclusive="both")]

if "price_bucket" in filtered_df.columns:
    options = [b for b in PRICE_BUCKET_ORDER if b in filtered_df["price_bucket"].dropna().astype(str).unique()]
    selected_buckets = st.sidebar.multiselect("Price bucket", options=options, default=options)
    if selected_buckets:
        filtered_df = filtered_df[filtered_df["price_bucket"].astype(str).isin(selected_buckets)]

m1, m2, m3 = st.columns(3)
m1.metric("Filtered Games", f"{len(filtered_df):,}")
if "Price" in filtered_df.columns:
    m2.metric("Median Price", f"${filtered_df['Price'].median():.2f}")
else:
    m2.metric("Median Price", "N/A")
if "positive_ratio" in filtered_df.columns:
    m3.metric("Median Positive Rate", f"{filtered_df['positive_ratio'].median():.1%}")
else:
    m3.metric("Median Positive Ratio", "N/A")

preview_cols = get_available_columns(
    filtered_df,
    ["Name", "release_year", "Price", "price_bucket", "owners_mid", "total_reviews", "positive_ratio"],
)
st.subheader("Filtered Dataset Preview")
if preview_cols:
    display_df = filtered_df[preview_cols].head(300).copy()
    if "owners_mid" in display_df.columns:
        display_df["owners_mid"] = display_df["owners_mid"].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
    if "total_reviews" in display_df.columns:
        display_df["total_reviews"] = display_df["total_reviews"].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
    if "positive_ratio" in display_df.columns:
        display_df["positive_ratio"] = display_df["positive_ratio"].map(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("No standard overview columns are available in the dataset.")
