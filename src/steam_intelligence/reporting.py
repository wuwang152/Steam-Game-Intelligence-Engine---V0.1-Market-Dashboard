"""Reporting utilities for reproducible market insights markdown outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

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

TABLE_CANDIDATE_COLUMNS = [
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


def to_numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(df.get(column, np.nan), errors="coerce")


def validate_required_columns(df: pd.DataFrame, required: list[str] | None = None) -> list[str]:
    expected = required or REQUIRED_V2_COLUMNS
    return [c for c in expected if c not in df.columns]


def format_int(value: Any) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{int(round(float(value))):,}"


def format_pct(value: Any) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.1%}"


def format_value_for_col(col: str, value: Any) -> str:
    if col == "positive_rate":
        return format_pct(value)
    if col in {"owners_mid", "total_reviews", "platform_count", "release_year"}:
        return format_int(value)
    if pd.isna(value):
        return "N/A"
    return str(value)


def distribution_table(series: pd.Series, key_name: str = "Category") -> pd.DataFrame:
    counts = series.fillna("Unknown").astype(str).value_counts(dropna=False)
    total = int(counts.sum())
    out = pd.DataFrame({key_name: counts.index, "Count": counts.values})
    out["Share"] = out["Count"] / total if total else np.nan
    return out


def build_markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows available._"
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in headers) + " |")
    return "\n".join(lines)


def prepare_rank_table(df: pd.DataFrame, sort_cols: list[str], ascending: list[bool], limit: int = 10) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    out = df.copy()
    for col in ["owners_mid", "total_reviews", "positive_rate", "platform_count", "release_year"]:
        out[col] = to_numeric_series(out, col)
    out = out.sort_values(sort_cols, ascending=ascending, na_position="last").head(limit)
    show = [c for c in TABLE_CANDIDATE_COLUMNS if c in out.columns]
    if not show:
        return pd.DataFrame()
    out = out[show].copy()
    for col in out.columns:
        out[col] = out[col].map(lambda v: format_value_for_col(col, v))
    return out


def compute_metrics(df: pd.DataFrame) -> dict[str, Any]:
    total_games = len(df)
    has_reviews = df.get("has_reviews", pd.Series(False, index=df.index)).fillna(False).astype(bool)
    reviewed = df[has_reviews]
    owners = to_numeric_series(df, "owners_mid")
    total_reviews = to_numeric_series(df, "total_reviews")
    positive_rate = to_numeric_series(df, "positive_rate")
    release_year = to_numeric_series(df, "release_year")
    platform_count = to_numeric_series(df, "platform_count")

    release_year_non_na = release_year.dropna()
    top_years = release_year_non_na.astype(int).value_counts().head(10).sort_values(ascending=False)

    return {
        "total_games": total_games,
        "games_with_reviews": int(has_reviews.sum()),
        "share_with_reviews": float(has_reviews.mean()) if total_games else np.nan,
        "median_owners_mid": owners.median(),
        "median_total_reviews": total_reviews.median(),
        "median_positive_rate_reviewed": to_numeric_series(reviewed, "positive_rate").median(),
        "free_share": float(df.get("is_free", pd.Series(False, index=df.index)).fillna(False).astype(bool).mean()) if total_games else np.nan,
        "discount_share": float(df.get("has_discount", pd.Series(False, index=df.index)).fillna(False).astype(bool).mean()) if total_games else np.nan,
        "price_bucket_dist": distribution_table(df.get("price_bucket", pd.Series(dtype=object)), "price_bucket"),
        "review_signal_dist": distribution_table(df.get("review_signal", pd.Series(dtype=object)), "review_signal"),
        "review_sentiment_dist": distribution_table(df.get("review_sentiment", pd.Series(dtype=object)), "review_sentiment"),
        "platform_count_dist": distribution_table(platform_count.fillna("Unknown"), "platform_count"),
        "release_year_min": release_year_non_na.min(),
        "release_year_max": release_year_non_na.max(),
        "top_release_years": top_years,
    }


def generate_hidden_gems(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["positive_rate"] = to_numeric_series(out, "positive_rate")
    out["total_reviews"] = to_numeric_series(out, "total_reviews")
    out["owners_mid"] = to_numeric_series(out, "owners_mid")
    candidates = out[(out["positive_rate"] >= 0.85) & (out["total_reviews"] >= 20)]
    if candidates.empty:
        return pd.DataFrame()
    owners_median = candidates["owners_mid"].median()
    gems = candidates[candidates["owners_mid"] <= owners_median]
    return prepare_rank_table(gems, ["positive_rate", "total_reviews"], [False, False], limit=10)


def render_report(df: pd.DataFrame, source_path: str) -> str:
    metrics = compute_metrics(df)
    min_reviews = max(20, int(np.nanmedian(to_numeric_series(df, "total_reviews"))) if to_numeric_series(df, "total_reviews").notna().any() else 20)
    rated = df[to_numeric_series(df, "total_reviews").fillna(0) >= min_reviews]

    top_owners = prepare_rank_table(df, ["owners_mid", "total_reviews"], [False, False], limit=10)
    top_reviews = prepare_rank_table(df, ["total_reviews", "owners_mid"], [False, False], limit=10)
    top_rated = prepare_rank_table(rated, ["positive_rate", "total_reviews"], [False, False], limit=10)
    hidden_gems = generate_hidden_gems(df)

    top_year_lines = "\n".join([f"- {int(year)}: {count:,} games" for year, count in metrics["top_release_years"].items()]) or "- N/A"

    return f"""# Steam Market Insights Report V0.2

## 1. Project Overview
This report summarizes descriptive V0.2 market analytics for the Steam Game Intelligence Engine.

## 2. Data and Analytical Features
The metrics in this document are computed from the available processed dataset file: `{source_path}`.
Required V0.2 analytical fields include release, ownership proxy, review, pricing, and platform features.

## 3. Executive Summary
- Total games: **{format_int(metrics['total_games'])}**
- Games with reviews: **{format_int(metrics['games_with_reviews'])}** ({format_pct(metrics['share_with_reviews'])})
- Median owners_mid (estimated ownership proxy): **{format_int(metrics['median_owners_mid'])}**
- Median total_reviews: **{format_int(metrics['median_total_reviews'])}**
- Median positive_rate among reviewed games: **{format_pct(metrics['median_positive_rate_reviewed'])}**
- Free game share: **{format_pct(metrics['free_share'])}**
- Discounted game share: **{format_pct(metrics['discount_share'])}**

## 4. Market Structure
- Release year range: **{format_int(metrics['release_year_min'])} to {format_int(metrics['release_year_max'])}**
- Top release years by game count:
{top_year_lines}

### Price Bucket Distribution
{build_markdown_table(metrics['price_bucket_dist'].assign(Count=metrics['price_bucket_dist']['Count'].map(format_int), Share=metrics['price_bucket_dist']['Share'].map(format_pct)))}

### Platform Count Distribution
{build_markdown_table(metrics['platform_count_dist'].assign(Count=metrics['platform_count_dist']['Count'].map(format_int), Share=metrics['platform_count_dist']['Share'].map(format_pct)))}

### Review Signal Distribution
{build_markdown_table(metrics['review_signal_dist'].assign(Count=metrics['review_signal_dist']['Count'].map(format_int), Share=metrics['review_signal_dist']['Share'].map(format_pct)))}

## 5. Pricing and Monetization
Pricing structure is described with `price_bucket`, `is_free`, and `has_discount` metrics from the available processed dataset.

## 6. Review and Popularity Signals
`positive_rate` is most meaningful for games with reviews. `review_log` and `total_reviews` are descriptive popularity proxies.

### Review Sentiment Distribution
{build_markdown_table(metrics['review_sentiment_dist'].assign(Count=metrics['review_sentiment_dist']['Count'].map(format_int), Share=metrics['review_sentiment_dist']['Share'].map(format_pct)))}

## 7. Top Games and Hidden Gems
### Top 10 Games by owners_mid
{build_markdown_table(top_owners)}

### Top 10 Games by total_reviews
{build_markdown_table(top_reviews)}

### Top 10 Rated Games by positive_rate (minimum {min_reviews} reviews)
{build_markdown_table(top_rated)}

### Potential Hidden Gems (Heuristic Candidates)
Heuristic only (not model predictions): positive_rate >= 85%, total_reviews >= 20, and owners_mid at or below candidate median.

{build_markdown_table(hidden_gems)}

## 8. Key Observations
In the available processed dataset, the market profile is summarized through descriptive distributions and ranking tables above.
These observations are descriptive and centered on estimated ownership proxy and review proxies.

## 9. Limitations
- `owners_mid` is an estimated midpoint of owner ranges, not exact sales.
- Estimated owners should not be interpreted as exact sales.
- Review counts and `positive_rate` are proxies for attention and reception.
- Dataset coverage depends on the raw source file.
- This V0.2 report is descriptive and does not include causal inference or machine learning predictions.

## 10. Next Steps
- Game segmentation
- Ranking score system
- Genre/tag opportunity analysis
- Predictive modeling later, after descriptive analysis is stable
"""


def write_report(markdown: str, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")
