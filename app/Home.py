"""Steam Game Intelligence Engine dashboard home page."""

import streamlit as st

from app.utils import format_percent, get_available_columns, require_processed_data

st.set_page_config(page_title="Steam Game Intelligence Engine", layout="wide")
st.title("Steam Game Intelligence Engine — V0.1")
st.caption("Beginner-friendly market dashboard built from cleaned Steam game data.")

st.write(
    "Use the pages in the sidebar to explore release trends, attention, pricing, reputation, and genre/tag patterns."
)

df = require_processed_data()

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("Total Games", f"{len(df):,}")

if "release_year" in df.columns and df["release_year"].notna().any():
    year_min = int(df["release_year"].min())
    year_max = int(df["release_year"].max())
    col2.metric("Release Year Range", f"{year_min}–{year_max}")
else:
    col2.metric("Release Year Range", "N/A")

if "Price" in df.columns:
    col3.metric("Median Price", f"${df['Price'].median():.2f}")
else:
    col3.metric("Median Price", "N/A")

if "positive_ratio" in df.columns:
    col4.metric("Median Positive Ratio", format_percent(df["positive_ratio"].median()))
else:
    col4.metric("Median Positive Ratio", "N/A")

if "total_reviews" in df.columns:
    col5.metric("Total Reviews", f"{int(df['total_reviews'].fillna(0).sum()):,}")
else:
    col5.metric("Total Reviews", "N/A")

if "Price" in df.columns and not df.empty:
    free_share = (df["Price"].fillna(0) == 0).mean()
    col6.metric("Free-Game Share", format_percent(free_share))
else:
    col6.metric("Free-Game Share", "N/A")

preview_columns = get_available_columns(
    df,
    [
        "Name",
        "release_year",
        "Price",
        "owners_mid",
        "total_reviews",
        "positive_ratio",
        "review_signal",
        "review_sentiment",
    ],
)

st.subheader("Dataset Preview")
if preview_columns:
    st.dataframe(df[preview_columns].head(30), use_container_width=True)
else:
    st.info("No preview columns were found in the processed dataset.")
