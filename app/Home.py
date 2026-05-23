"""Steam Game Intelligence Engine dashboard home page."""

from __future__ import annotations

import io

import pandas as pd
import streamlit as st

from app.utils import load_processed_data, top_split_values

st.set_page_config(page_title="Steam Game Intelligence Engine", layout="wide")


def _to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


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

    if "release_year" in filtered.columns and filtered["release_year"].notna().any():
        years = _to_numeric(filtered["release_year"])
        year_min = int(years.min())
        year_max = int(years.max())
        selected_years = st.sidebar.slider("Release year", year_min, year_max, (year_min, year_max))
        filtered = filtered[years.between(selected_years[0], selected_years[1], inclusive="both")]

    if "Price" in filtered.columns and filtered["Price"].notna().any():
        prices = _to_numeric(filtered["Price"]).fillna(0)
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

    genre_col = "Genres" if "Genres" in filtered.columns else ("genres" if "genres" in filtered.columns else None)
    if genre_col:
        genre_counts = top_split_values(filtered, genre_col, sep=";", top_n=200)
        genre_options = genre_counts.index.tolist()
        selected_genres = st.sidebar.multiselect("Genres", options=genre_options)
        if selected_genres:
            genre_pattern = "|".join(selected_genres)
            genre_series = filtered[genre_col].fillna("").astype(str)
            filtered = filtered[genre_series.str.contains(genre_pattern, case=False, regex=True)]

    if "positive" in filtered.columns and filtered["positive"].notna().any():
        positives = _to_numeric(filtered["positive"]).fillna(0)
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

    k1.metric("Total games", f"{len(df):,}")

    if "Price" in df.columns and df["Price"].notna().any():
        k2.metric("Median price", f"${_to_numeric(df['Price']).median():.2f}")
    else:
        k2.metric("Median price", "N/A")

    if "owners_mid" in df.columns and df["owners_mid"].notna().any():
        k3.metric("Median owners", f"{int(_to_numeric(df['owners_mid']).median()):,}")
    else:
        k3.metric("Median owners", "N/A")

    if "peak_ccu" in df.columns and df["peak_ccu"].notna().any():
        k4.metric("Average peak CCU", f"{_to_numeric(df['peak_ccu']).mean():,.0f}")
    else:
        k4.metric("Average peak CCU", "N/A")

    if "positive" in df.columns and df["positive"].notna().any():
        k5.metric("Average positive reviews", f"{_to_numeric(df['positive']).mean():,.0f}")
    else:
        k5.metric("Average positive reviews", "N/A")

    if "release_year" in df.columns and df["release_year"].notna().any():
        years = _to_numeric(df["release_year"])
        k6.metric("Release year range", f"{int(years.min())}–{int(years.max())}")
    else:
        k6.metric("Release year range", "N/A")


def _show_charts(df: pd.DataFrame) -> None:
    st.subheader("Market exploration")
    c1, c2 = st.columns(2)

    if "release_year" in df.columns and df["release_year"].notna().any():
        by_year = _to_numeric(df["release_year"]).dropna().astype(int).value_counts().sort_index()
        c1.bar_chart(by_year, x_label="Release year", y_label="Games")
    else:
        c1.info("Release year column unavailable for yearly release chart.")

    if "Price" in df.columns and df["Price"].notna().any():
        price_data = _to_numeric(df["Price"]).dropna()
        c2.bar_chart(price_data.value_counts(bins=20).sort_index(), x_label="Price bins", y_label="Games")
    else:
        c2.info("Price column unavailable for price distribution chart.")

    c3, c4 = st.columns(2)
    genre_col = "Genres" if "Genres" in df.columns else ("genres" if "genres" in df.columns else None)
    if genre_col:
        top_genres = top_split_values(df, genre_col, sep=";", top_n=10)
        c3.bar_chart(top_genres, x_label="Genre", y_label="Games")
    else:
        c3.info("Genres column unavailable for top-genre chart.")

    if {"owners_mid", "positive"}.issubset(df.columns):
        scatter_df = df[["owners_mid", "positive"]].copy()
        scatter_df["owners_mid"] = _to_numeric(scatter_df["owners_mid"])
        scatter_df["positive"] = _to_numeric(scatter_df["positive"])
        scatter_df = scatter_df.dropna()
        if not scatter_df.empty:
            c4.scatter_chart(scatter_df, x="owners_mid", y="positive")
        else:
            c4.info("Owners/positive columns are present but contain no plottable values.")
    else:
        c4.info("owners_mid and positive columns are required for the scatter plot.")


def _show_table(df: pd.DataFrame) -> None:
    st.subheader("Filtered games")
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        "Download filtered CSV",
        data=csv_buffer.getvalue(),
        file_name="steam_games_filtered.csv",
        mime="text/csv",
    )


def main() -> None:
    st.title("Steam Game Intelligence Engine — V0.1")
    st.caption("Interactive market exploration dashboard for cleaned Steam games data.")
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
