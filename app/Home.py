"""Steam Game Intelligence Engine dashboard home page."""

from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from app.utils import load_processed_data, top_split_values

st.set_page_config(page_title="Steam Game Intelligence Engine", layout="wide")


PREVIEW_COLUMNS = [
    "Name",
    "release_year",
    "Price",
    "owners_mid",
    "total_reviews",
    "positive_ratio",
    "review_signal",
    "review_sentiment",
    "Genres",
    "Tags",
]


def _to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _resolve_column(df: pd.DataFrame, aliases: list[str]) -> str | None:
    for alias in aliases:
        if alias in df.columns:
            return alias
    return None


def _resolve_platform_columns(df: pd.DataFrame) -> dict[str, str]:
    candidates = {
        "Windows": ["Windows", "windows"],
        "Mac": ["Mac", "mac"],
        "Linux": ["Linux", "linux"],
    }
    resolved: dict[str, str] = {}
    for label, names in candidates.items():
        for name in names:
            if name in df.columns:
                resolved[label] = name
                break
    return resolved


def _apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    filtered = df.copy()

    release_year_col = _resolve_column(filtered, ["release_year", "Release Year"])
    price_col = _resolve_column(filtered, ["Price", "price"])
    genre_col = _resolve_column(filtered, ["Genres", "genres"])
    positive_col = _resolve_column(filtered, ["positive", "Positive"])

    if release_year_col and filtered[release_year_col].notna().any():
        years = _to_numeric(filtered[release_year_col])
        year_min = int(years.min())
        year_max = int(years.max())
        selected_years = st.sidebar.slider("Release year", year_min, year_max, (year_min, year_max))
        filtered = filtered[years.between(selected_years[0], selected_years[1], inclusive="both")]

    if price_col and filtered[price_col].notna().any():
        prices = _to_numeric(filtered[price_col]).fillna(0)
        price_min = float(prices.min())
        price_max = float(prices.max())
        selected_price = st.sidebar.slider(
            "Price range (USD)",
            min_value=price_min,
            max_value=price_max,
            value=(price_min, price_max),
            step=0.5,
        )
        filtered = filtered[prices.between(selected_price[0], selected_price[1], inclusive="both")]

    platform_cols = _resolve_platform_columns(filtered)
    if platform_cols:
        selected_platforms = st.sidebar.multiselect(
            "Platform availability",
            options=list(platform_cols.keys()),
            default=list(platform_cols.keys()),
        )
        if selected_platforms:
            mask = pd.Series(False, index=filtered.index)
            for platform in selected_platforms:
                col = platform_cols[platform]
                values = filtered[col]
                if pd.api.types.is_bool_dtype(values):
                    platform_mask = values.fillna(False)
                else:
                    platform_mask = values.astype(str).str.lower().isin(["true", "1", "yes"])
                mask = mask | platform_mask
            filtered = filtered[mask]

    if genre_col:
        genre_counts = top_split_values(filtered, genre_col, sep=";", top_n=200)
        genre_options = genre_counts.index.tolist()
        selected_genres = st.sidebar.multiselect("Genres", options=genre_options)
        if selected_genres:
            genre_pattern = "|".join(selected_genres)
            genre_series = filtered[genre_col].fillna("").astype(str)
            filtered = filtered[genre_series.str.contains(genre_pattern, case=False, regex=True)]

    if positive_col and filtered[positive_col].notna().any():
        positives = _to_numeric(filtered[positive_col]).fillna(0)
        min_positive = int(positives.min())
        max_positive = int(positives.max())
        selected_min_positive = st.sidebar.slider(
            "Minimum positive reviews",
            min_value=min_positive,
            max_value=max_positive,
            value=min_positive,
        )
        filtered = filtered[positives >= selected_min_positive]

    return filtered


def _show_kpis(df: pd.DataFrame) -> None:
    st.subheader("Key metrics")
    k1, k2, k3 = st.columns(3)
    k4, k5, k6 = st.columns(3)

    price_col = _resolve_column(df, ["Price", "price"])
    owners_col = _resolve_column(df, ["owners_mid", "Owners Mid"])
    peak_ccu_col = _resolve_column(df, ["peak_ccu", "Peak CCU", "Peak_CCU"])
    positive_col = _resolve_column(df, ["positive", "Positive"])
    release_year_col = _resolve_column(df, ["release_year", "Release Year"])

    k1.metric("Total games", f"{len(df):,}")

    if price_col and df[price_col].notna().any():
        k2.metric("Median price", f"${_to_numeric(df[price_col]).median():.2f}")
    else:
        k2.metric("Median price", "N/A")

    if owners_col and df[owners_col].notna().any():
        k3.metric("Estimated Owners Midpoint (Median)", f"{int(_to_numeric(df[owners_col]).median()):,}")
    else:
        k3.metric("Estimated Owners Midpoint (Median)", "N/A")

    if peak_ccu_col and df[peak_ccu_col].notna().any():
        k4.metric("Average peak CCU", f"{_to_numeric(df[peak_ccu_col]).mean():,.0f}")
    else:
        k4.metric("Average peak CCU", "N/A")

    if positive_col and df[positive_col].notna().any():
        k5.metric("Average positive reviews", f"{_to_numeric(df[positive_col]).mean():,.0f}")
    else:
        k5.metric("Average positive reviews", "N/A")

    if release_year_col and df[release_year_col].notna().any():
        years = _to_numeric(df[release_year_col])
        k6.metric("Release year range", f"{int(years.min())}–{int(years.max())}")
    else:
        k6.metric("Release year range", "N/A")


def _show_charts(df: pd.DataFrame) -> None:
    st.subheader("Market exploration")
    c1, c2 = st.columns(2)

    release_year_col = _resolve_column(df, ["release_year", "Release Year"])
    price_col = _resolve_column(df, ["Price", "price"])
    genre_col = _resolve_column(df, ["Genres", "genres"])
    owners_col = _resolve_column(df, ["owners_mid", "Owners Mid"])
    positive_col = _resolve_column(df, ["positive", "Positive"])

    if release_year_col and df[release_year_col].notna().any():
        by_year = _to_numeric(df[release_year_col]).dropna().astype(int).value_counts().sort_index()
        c1.bar_chart(by_year, x_label="Release year", y_label="Games")
    else:
        c1.info("Release year column unavailable for yearly release chart.")

    if price_col and df[price_col].notna().any():
        price_data = _to_numeric(df[price_col]).dropna()
        if not price_data.empty:
            bins = [-0.01, 0.01, 5, 10, 20, 50, float("inf")]
            labels = ["$0", "$0–5", "$5–10", "$10–20", "$20–50", "$50+"]
            bucketed = pd.cut(price_data, bins=bins, labels=labels, include_lowest=True, right=True)
            counts = bucketed.value_counts(sort=False)
            c2.bar_chart(counts, x_label="Price bucket", y_label="Games")
        else:
            c2.info("Price column unavailable for price distribution chart.")
    else:
        c2.info("Price column unavailable for price distribution chart.")

    c3, c4 = st.columns(2)
    if genre_col:
        top_genres = top_split_values(df, genre_col, sep=";", top_n=10)
        c3.bar_chart(top_genres, x_label="Genre", y_label="Games")
    else:
        c3.info("Genres column unavailable for top-genre chart.")

    if owners_col and positive_col:
        scatter_df = df[[owners_col, positive_col]].copy()
        scatter_df[owners_col] = _to_numeric(scatter_df[owners_col])
        scatter_df[positive_col] = _to_numeric(scatter_df[positive_col])
        scatter_df = scatter_df.dropna()
        if not scatter_df.empty:
            c4.scatter_chart(scatter_df, x=owners_col, y=positive_col)
        else:
            c4.info("Owners/positive columns are present but contain no plottable values.")
    else:
        c4.info("owners_mid and positive columns are required for the scatter plot.")


def _show_table(df: pd.DataFrame) -> None:
    st.subheader("Filtered games")
    available_preview_cols = [column for column in PREVIEW_COLUMNS if column in df.columns]
    preview_df = df[available_preview_cols].copy() if available_preview_cols else df.copy()
    preview_rows = min(len(preview_df), 500)
    st.caption(f"Showing first {preview_rows:,} rows of {len(df):,} filtered games")
    st.dataframe(preview_df.head(500), use_container_width=True, hide_index=True)

    csv_buffer = io.StringIO()
    preview_df.to_csv(csv_buffer, index=False)
    st.download_button(
        "Download filtered CSV",
        data=csv_buffer.getvalue(),
        file_name="steam_games_filtered.csv",
        mime="text/csv",
    )


def main() -> None:
    st.title("Steam Game Intelligence Engine — V0.2")
    st.caption(
        "V0.2 includes analytical feature engineering, Market Insights, and reproducible report generation."
    )
    st.write(
        "Filter games by release timing, price, platform, genre, and review momentum to identify market patterns quickly."
    )

    df = load_processed_data()
    if df is None:
        st.warning(
            "Processed dataset not found at `data/processed/steam_games_cleaned.csv`. "
            "Run `PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv "
            "--output data/processed/steam_games_cleaned.csv` before using this dashboard."
        )
        st.stop()

    filtered_df = _apply_filters(df)
    _show_kpis(filtered_df)
    _show_charts(filtered_df)
    _show_table(filtered_df)


main()
