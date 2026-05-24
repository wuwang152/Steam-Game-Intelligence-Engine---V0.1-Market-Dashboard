import numpy as np
import pandas as pd
import streamlit as st

from app.utils import get_available_columns, require_processed_data, safe_column

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

TABLE_COLUMNS = [
    "Name",
    "release_year",
    "price_bucket",
    "owners_mid",
    "total_reviews",
    "positive_rate",
    "platform_count",
    "Genres",
    "Tags",
]
PRICE_BUCKET_ORDER = ["free", "budget", "mid", "premium", "luxury"]
REVIEW_SIGNAL_ORDER = ["no_signal", "very_low", "low", "medium", "high"]
REVIEW_SENTIMENT_ORDER = ["no_reviews", "weak", "mixed", "strong"]
PLATFORM_COUNT_ORDER = [0, 1, 2, 3]


def numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(safe_column(df, column, np.nan), errors="coerce")


def format_int(value) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{int(round(float(value))):,}"


def format_percent_safe(value) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.1%}"


def safe_share(mask: pd.Series) -> float:
    if len(mask) == 0:
        return np.nan
    return float(mask.fillna(False).mean())


def prepare_display_table(df: pd.DataFrame, sort_cols: list[str], ascending: list[bool], limit: int = 20) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()
    for col in ["owners_mid", "total_reviews", "positive_rate", "platform_count", "release_year"]:
        out[col] = numeric_series(out, col)

    out = out.sort_values(sort_cols, ascending=ascending, na_position="last").head(limit)
    show_cols = get_available_columns(out, TABLE_COLUMNS)
    if not show_cols:
        return pd.DataFrame()

    display_df = out[show_cols].copy()
    if "release_year" in display_df.columns:
        display_df["release_year"] = display_df["release_year"].map(format_int)
    if "owners_mid" in display_df.columns:
        display_df["owners_mid"] = display_df["owners_mid"].map(format_int)
    if "total_reviews" in display_df.columns:
        display_df["total_reviews"] = display_df["total_reviews"].map(format_int)
    if "positive_rate" in display_df.columns:
        display_df["positive_rate"] = display_df["positive_rate"].map(format_percent_safe)
    if "platform_count" in display_df.columns:
        display_df["platform_count"] = display_df["platform_count"].map(format_int)

    return display_df


st.title("Market Insights")
st.info("V0.2 analytical features are used on this page.")


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
selected_years = None
selected_buckets = []
review_floor = 0
selected_platform_range = None

if filtered_df["release_year"].notna().any():
    valid_years = numeric_series(filtered_df, "release_year").dropna()
    if not valid_years.empty:
        y_min = int(valid_years.min())
        y_max = int(valid_years.max())
        selected_years = st.sidebar.slider("Release year", min_value=y_min, max_value=y_max, value=(y_min, y_max))
        filtered_df = filtered_df[numeric_series(filtered_df, "release_year").between(*selected_years)]

bucket_options = sorted(filtered_df["price_bucket"].dropna().astype(str).unique().tolist())
bucket_options = [b for b in PRICE_BUCKET_ORDER if b in bucket_options] + [b for b in bucket_options if b not in PRICE_BUCKET_ORDER]
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

platform_values = numeric_series(filtered_df, "platform_count").dropna()
if not platform_values.empty:
    p_min, p_max = int(platform_values.min()), int(platform_values.max())
    selected_platform_range = st.sidebar.slider("Platform count", min_value=p_min, max_value=p_max, value=(p_min, p_max))
    filtered_df = filtered_df[numeric_series(filtered_df, "platform_count").between(*selected_platform_range)]

reviews_values = numeric_series(filtered_df, "total_reviews").dropna()
if not reviews_values.empty:
    review_floor = st.sidebar.slider("Minimum total_reviews", min_value=0, max_value=int(reviews_values.max()), value=0)
    filtered_df = filtered_df[numeric_series(filtered_df, "total_reviews").fillna(0) >= review_floor]

st.caption(
    "Filter summary: "
    f"{len(filtered_df):,} games | "
    f"Release years: {f'{selected_years[0]}–{selected_years[1]}' if selected_years else 'All'} | "
    f"Price buckets: {', '.join(selected_buckets) if selected_buckets else 'All'} | "
    f"Minimum total_reviews: {review_floor:,}"
)

if filtered_df.empty:
    st.warning("No games match the current filters. Try relaxing release year, review minimum, or price bucket selections.")
    st.stop()

st.subheader("Executive KPIs")
k1, k2, k3, k4, k5, k6 = st.columns(6)
with_reviews = filtered_df[safe_column(filtered_df, "has_reviews", False).fillna(False)]
k1.metric("Total games", format_int(len(filtered_df)))
k2.metric("Games with reviews", format_int(safe_column(filtered_df, "has_reviews", False).fillna(False).sum()))
k3.metric("Median owners_mid (estimated)", format_int(numeric_series(filtered_df, "owners_mid").median()))
k4.metric("Median Positive Rate", format_percent_safe(numeric_series(with_reviews, "positive_rate").median()))
k5.metric("Free game share", format_percent_safe(safe_share(safe_column(filtered_df, "is_free", False))))
k6.metric("Discounted game share", format_percent_safe(safe_share(safe_column(filtered_df, "has_discount", False))))
st.caption("KPIs are computed from the currently filtered sample and use robust missing-value handling.")

market_tab, review_tab, ranking_tab = st.tabs(["Market Structure", "Review & Popularity", "Rankings"])

with market_tab:
    st.subheader("Market Structure")

    st.caption("Games by release_year: yearly game count after filters.")
    st.caption("Recent and future release years may be incomplete.")
    year_counts = numeric_series(filtered_df, "release_year").dropna().astype(int).value_counts().sort_index()
    if not year_counts.empty:
        st.bar_chart(year_counts)
    else:
        st.info("No release year data available for current filters.")

    st.caption("Price Bucket distribution: game count by pricing segment.")
    bucket_series = safe_column(filtered_df, "price_bucket", "Unknown").fillna("Unknown").astype(str)
    bucket_order = [x for x in PRICE_BUCKET_ORDER if x in bucket_series.unique()]
    bucket_remainder = sorted([x for x in bucket_series.unique() if x not in bucket_order])
    bucket_counts = bucket_series.value_counts().reindex(bucket_order + bucket_remainder, fill_value=0)
    if not bucket_counts.empty:
        st.bar_chart(bucket_counts)
    else:
        st.info("No price bucket data available for current filters.")

    st.caption("Estimated Ownership Tier Distribution")
    owners_dist = numeric_series(filtered_df, "owners_mid").dropna()
    if not owners_dist.empty:
        bins = [-0.1, 0, 10_000, 50_000, 100_000, 500_000, 1_000_000, 10_000_000, np.inf]
        labels = ["0", "1–10k", "10k–50k", "50k–100k", "100k–500k", "500k–1M", "1M–10M", "10M+"]
        owners_tier = pd.cut(owners_dist, bins=bins, labels=labels, include_lowest=True, right=True)
        st.bar_chart(owners_tier.value_counts(sort=False))
        st.caption("owners_mid is an estimated midpoint of owner ranges, not exact sales.")
    else:
        st.info("No valid owners_mid values available for distribution plotting.")

    st.caption("Review Signal distribution: quality/volume signal buckets from V0.2 features.")
    signal_series = safe_column(filtered_df, "review_signal", "Unknown").fillna("Unknown").astype(str)
    signal_order = [x for x in REVIEW_SIGNAL_ORDER if x in signal_series.unique()]
    signal_remainder = sorted([x for x in signal_series.unique() if x not in signal_order])
    signal_counts = signal_series.value_counts().reindex(signal_order + signal_remainder, fill_value=0)
    if not signal_counts.empty:
        st.bar_chart(signal_counts)
    else:
        st.info("No review_signal values available for current filters.")

    st.caption("Review Sentiment distribution: sentiment group counts for filtered games.")
    sentiment_series = safe_column(filtered_df, "review_sentiment", "Unknown").fillna("Unknown").astype(str)
    sentiment_order = [x for x in REVIEW_SENTIMENT_ORDER if x in sentiment_series.unique()]
    sentiment_remainder = sorted([x for x in sentiment_series.unique() if x not in sentiment_order])
    sentiment_counts = sentiment_series.value_counts().reindex(sentiment_order + sentiment_remainder, fill_value=0)
    if not sentiment_counts.empty:
        st.bar_chart(sentiment_counts)
    else:
        st.info("No review_sentiment values available for current filters.")

with review_tab:
    st.subheader("Review and Popularity")

    st.caption("owners_mid vs Positive Rate for reviewed games: ownership scale and sentiment relationship.")
    st.caption("Positive Rate is most meaningful for games with reviews.")
    scatter_a = filtered_df[
        safe_column(filtered_df, "has_reviews", False).fillna(False)
        & numeric_series(filtered_df, "owners_mid").notna()
        & numeric_series(filtered_df, "positive_rate").notna()
    ][["owners_mid", "positive_rate"]].copy()
    if not scatter_a.empty:
        scatter_a["owners_mid"] = pd.to_numeric(scatter_a["owners_mid"], errors="coerce")
        scatter_a = scatter_a.sort_values("owners_mid")
        st.scatter_chart(scatter_a, x="owners_mid", y="positive_rate")
    else:
        st.info("No valid rows for owners_mid vs positive_rate under current filters.")

    st.caption("review_log vs positive_rate for reviewed games: review volume signal versus sentiment.")
    scatter_b = filtered_df[
        safe_column(filtered_df, "has_reviews", False).fillna(False)
        & numeric_series(filtered_df, "review_log").notna()
        & numeric_series(filtered_df, "positive_rate").notna()
    ][["review_log", "positive_rate"]].copy()
    if not scatter_b.empty:
        st.scatter_chart(scatter_b, x="review_log", y="positive_rate")
    else:
        st.info("No valid rows for review_log vs positive_rate under current filters.")

with ranking_tab:
    st.subheader("Top Games")
    st.caption("Top-game tables are ranked on numeric conversions with display-only formatting.")

    top_owners_df = prepare_display_table(filtered_df, ["owners_mid", "total_reviews"], [False, False], limit=20)
    st.caption("Top games by Estimated Owners Midpoint")
    if top_owners_df.empty:
        st.info("No rows available for owners_mid ranking under current filters.")
    else:
        st.dataframe(top_owners_df, use_container_width=True)

    top_reviews_df = prepare_display_table(filtered_df, ["total_reviews", "owners_mid"], [False, False], limit=20)
    st.caption("Top games by Total Reviews")
    if top_reviews_df.empty:
        st.info("No rows available for total_reviews ranking under current filters.")
    else:
        st.dataframe(top_reviews_df, use_container_width=True)

    min_reviews_for_rating = max(20, int(numeric_series(filtered_df, "total_reviews").median()) if numeric_series(filtered_df, "total_reviews").notna().any() else 20)
    top_rated = filtered_df[numeric_series(filtered_df, "total_reviews").fillna(0) >= min_reviews_for_rating].copy()
    top_rated_df = prepare_display_table(top_rated, ["positive_rate", "total_reviews"], [False, False], limit=20)
    st.caption(f"Top rated games by Positive Rate (minimum {min_reviews_for_rating:,} reviews)")
    if top_rated_df.empty:
        st.info("No games satisfy the minimum review threshold for rated ranking.")
    else:
        st.dataframe(top_rated_df, use_container_width=True)

    st.subheader("Hidden Gems")
    st.caption(
        "Hidden Gems: Heuristic candidates, not model predictions."
    )
    hidden_gems = filtered_df[
        (numeric_series(filtered_df, "positive_rate") >= 0.85)
        & (numeric_series(filtered_df, "total_reviews") >= 20)
    ].copy()
    if not hidden_gems.empty:
        owner_cutoff = numeric_series(hidden_gems, "owners_mid").median()
        hidden_gems = hidden_gems[numeric_series(hidden_gems, "owners_mid") <= owner_cutoff]

    hidden_gems_df = prepare_display_table(hidden_gems, ["positive_rate", "total_reviews"], [False, False], limit=20)
    st.caption("Potential hidden gems")
    if hidden_gems_df.empty:
        st.info("No hidden gem candidates found under current filters.")
    else:
        st.dataframe(hidden_gems_df, use_container_width=True)
