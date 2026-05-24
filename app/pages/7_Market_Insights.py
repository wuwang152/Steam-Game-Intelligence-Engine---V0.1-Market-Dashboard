import numpy as np
import pandas as pd
import streamlit as st

from app.utils import format_percent, get_available_columns, require_processed_data, safe_column

REQUIRED_V2_COLUMNS = [
    "release_year",
    "owners_mid",
    "total_reviews",
    "positive_rate",
    "review_log",
    "has_reviews",
    "is_free",
    "has_discount",
    "platform_count",
    "price_bucket",
    "review_signal",
    "review_sentiment",
]


def format_int(value) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{int(round(float(value))):,}"


def safe_share(mask: pd.Series) -> float:
    if len(mask) == 0:
        return np.nan
    return float(mask.fillna(False).mean())


st.title("Market Insights")
st.caption(
    "Use V0.2 analytical features to explore Steam market structure, popularity, reviews, pricing, and release patterns."
)

df = require_processed_data()
missing_required = [col for col in REQUIRED_V2_COLUMNS if col not in df.columns]
if missing_required:
    st.error(
        "This page requires V0.2 analytical features. Missing columns: "
        + ", ".join(missing_required)
        + ". Run the pipeline again to regenerate processed data."
    )
    st.stop()

filtered_df = df.copy()
st.sidebar.header("Market Insights Filters")

if filtered_df["release_year"].notna().any():
    valid_years = pd.to_numeric(filtered_df["release_year"], errors="coerce").dropna()
    if not valid_years.empty:
        y_min = int(valid_years.min())
        y_max = int(valid_years.max())
        selected_years = st.sidebar.slider("Release year", min_value=y_min, max_value=y_max, value=(y_min, y_max))
        filtered_df = filtered_df[pd.to_numeric(filtered_df["release_year"], errors="coerce").between(*selected_years)]

bucket_options = sorted(filtered_df["price_bucket"].dropna().astype(str).unique().tolist())
if bucket_options:
    selected_buckets = st.sidebar.multiselect("Price bucket", options=bucket_options, default=bucket_options)
    if selected_buckets:
        filtered_df = filtered_df[filtered_df["price_bucket"].astype(str).isin(selected_buckets)]

has_reviews_opt = st.sidebar.selectbox("Has reviews", options=["All", "Yes", "No"], index=0)
if has_reviews_opt != "All":
    expected = has_reviews_opt == "Yes"
    filtered_df = filtered_df[safe_column(filtered_df, "has_reviews", False).fillna(False) == expected]

is_free_opt = st.sidebar.selectbox("Free to play", options=["All", "Free", "Paid"], index=0)
if is_free_opt != "All":
    expected = is_free_opt == "Free"
    filtered_df = filtered_df[safe_column(filtered_df, "is_free", False).fillna(False) == expected]

platform_values = pd.to_numeric(filtered_df["platform_count"], errors="coerce").dropna()
if not platform_values.empty:
    p_min, p_max = int(platform_values.min()), int(platform_values.max())
    selected_platform_range = st.sidebar.slider("Platform count", min_value=p_min, max_value=p_max, value=(p_min, p_max))
    filtered_df = filtered_df[pd.to_numeric(filtered_df["platform_count"], errors="coerce").between(*selected_platform_range)]

reviews_values = pd.to_numeric(filtered_df["total_reviews"], errors="coerce").dropna()
if not reviews_values.empty:
    review_floor = st.sidebar.slider("Minimum total_reviews", min_value=0, max_value=int(reviews_values.max()), value=0)
    filtered_df = filtered_df[pd.to_numeric(filtered_df["total_reviews"], errors="coerce").fillna(0) >= review_floor]

if filtered_df.empty:
    st.warning("No games match the selected filters. Adjust the sidebar filters to continue.")
    st.stop()

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total games", format_int(len(filtered_df)))
k2.metric("Games with reviews", format_int(safe_column(filtered_df, "has_reviews", False).fillna(False).sum()))
k3.metric("Median owners_mid", format_int(pd.to_numeric(filtered_df["owners_mid"], errors="coerce").median()))
with_reviews = filtered_df[safe_column(filtered_df, "has_reviews", False).fillna(False)]
k4.metric("Median positive_rate", format_percent(pd.to_numeric(with_reviews["positive_rate"], errors="coerce").median()))
k5.metric("Free game share", format_percent(safe_share(safe_column(filtered_df, "is_free", False))))
k6.metric("Discounted game share", format_percent(safe_share(safe_column(filtered_df, "has_discount", False))))

st.subheader("Market Structure")
year_counts = filtered_df["release_year"].dropna().astype(int).value_counts().sort_index()
if not year_counts.empty:
    st.caption("Games by release year")
    st.bar_chart(year_counts)
else:
    st.info("No release_year data available for the current filters.")

bucket_counts = filtered_df["price_bucket"].fillna("Unknown").astype(str).value_counts()
if not bucket_counts.empty:
    st.caption("Distribution of price buckets")
    st.bar_chart(bucket_counts)

owners_dist = pd.to_numeric(filtered_df["owners_mid"], errors="coerce").dropna()
if not owners_dist.empty:
    st.caption("Distribution of log10(owners_mid + 1)")
    owners_hist = pd.Series(np.log10(owners_dist + 1), name="log10_owners_mid")
    st.bar_chart(owners_hist.value_counts(bins=30).sort_index())

signal_counts = filtered_df["review_signal"].fillna("Unknown").astype(str).value_counts()
if not signal_counts.empty:
    st.caption("Distribution of review_signal")
    st.bar_chart(signal_counts)

sentiment_counts = filtered_df["review_sentiment"].fillna("Unknown").astype(str).value_counts()
if not sentiment_counts.empty:
    st.caption("Distribution of review_sentiment")
    st.bar_chart(sentiment_counts)

st.subheader("Review and Popularity Analysis")
scatter_a = filtered_df[
    safe_column(filtered_df, "has_reviews", False).fillna(False)
    & pd.to_numeric(filtered_df["owners_mid"], errors="coerce").notna()
    & pd.to_numeric(filtered_df["positive_rate"], errors="coerce").notna()
][["owners_mid", "positive_rate"]].copy()
if not scatter_a.empty:
    scatter_a["owners_mid"] = pd.to_numeric(scatter_a["owners_mid"], errors="coerce")
    scatter_a = scatter_a.sort_values("owners_mid")
    st.caption("owners_mid vs positive_rate (reviews-only games)")
    st.scatter_chart(scatter_a, x="owners_mid", y="positive_rate")
else:
    st.info("No valid rows for owners_mid vs positive_rate under current filters.")

scatter_b = filtered_df[
    safe_column(filtered_df, "has_reviews", False).fillna(False)
    & pd.to_numeric(filtered_df["review_log"], errors="coerce").notna()
    & pd.to_numeric(filtered_df["positive_rate"], errors="coerce").notna()
][["review_log", "positive_rate"]].copy()
if not scatter_b.empty:
    st.caption("review_log vs positive_rate (reviews-only games)")
    st.scatter_chart(scatter_b, x="review_log", y="positive_rate")
else:
    st.info("No valid rows for review_log vs positive_rate under current filters.")

st.subheader("Top Games")
base_cols = ["Name", "release_year", "price_bucket", "owners_mid", "total_reviews", "positive_rate", "platform_count", "Genres", "Tags"]
show_cols = get_available_columns(filtered_df, base_cols)

if show_cols:
    top_owners = filtered_df.sort_values("owners_mid", ascending=False).head(20)
    st.caption("Top games by owners_mid")
    st.dataframe(top_owners[show_cols], use_container_width=True)

    top_reviews = filtered_df.sort_values("total_reviews", ascending=False).head(20)
    st.caption("Top games by total_reviews")
    st.dataframe(top_reviews[show_cols], use_container_width=True)

    min_reviews_for_rating = max(20, int(filtered_df["total_reviews"].median()) if filtered_df["total_reviews"].notna().any() else 20)
    top_rated = filtered_df[pd.to_numeric(filtered_df["total_reviews"], errors="coerce").fillna(0) >= min_reviews_for_rating]
    top_rated = top_rated.sort_values(["positive_rate", "total_reviews"], ascending=[False, False]).head(20)
    st.caption(f"Top rated games by positive_rate (minimum {min_reviews_for_rating} reviews)")
    st.dataframe(top_rated[show_cols], use_container_width=True)

    hidden_gems = filtered_df[
        (pd.to_numeric(filtered_df["positive_rate"], errors="coerce") >= 0.85)
        & (pd.to_numeric(filtered_df["total_reviews"], errors="coerce") >= 20)
    ].copy()
    if not hidden_gems.empty:
        owner_cutoff = hidden_gems["owners_mid"].median()
        hidden_gems = hidden_gems[pd.to_numeric(hidden_gems["owners_mid"], errors="coerce") <= owner_cutoff]
    hidden_gems = hidden_gems.sort_values(["positive_rate", "total_reviews"], ascending=[False, False]).head(20)
    st.caption("Potential hidden gems (high positive_rate with relatively lower owners_mid)")
    if hidden_gems.empty:
        st.info("No hidden gems found under current filters.")
    else:
        st.dataframe(hidden_gems[show_cols], use_container_width=True)
else:
    st.info("No standard table columns are available in the current dataset.")
