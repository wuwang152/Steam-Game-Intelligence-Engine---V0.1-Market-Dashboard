"""Feature engineering helpers for Steam market analytics."""

from __future__ import annotations

import pandas as pd


def _split_owner_range(value: str) -> tuple[float, float]:
    """Split owner range strings like '20,000 - 50,000' into numeric bounds."""
    if pd.isna(value):
        return float("nan"), float("nan")

    text = str(value).replace(",", "")
    if "-" not in text:
        return float("nan"), float("nan")

    low_text, high_text = [piece.strip() for piece in text.split("-", maxsplit=1)]
    try:
        return float(low_text), float(high_text)
    except ValueError:
        return float("nan"), float("nan")


def _count_pipe_items(value: str) -> int:
    """Count list-like values separated by ';' or ',' in a robust way."""
    if pd.isna(value) or str(value).strip() == "":
        return 0

    text = str(value)
    sep = ";" if ";" in text else ","
    items = [item.strip() for item in text.split(sep) if item.strip()]
    return len(items)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create V0.1 engineered features required for dashboard analytics."""
    out = df.copy()

    out["release_year"] = pd.to_datetime(out["Release date"], errors="coerce").dt.year

    owner_bounds = out["Estimated owners"].apply(_split_owner_range)
    out["owners_low"] = owner_bounds.apply(lambda x: x[0])
    out["owners_high"] = owner_bounds.apply(lambda x: x[1])
    out["owners_mid"] = (out["owners_low"] + out["owners_high"]) / 2

    out["total_reviews"] = out["Positive"].fillna(0) + out["Negative"].fillna(0)
    out["positive_ratio"] = out["Positive"].fillna(0) / out["total_reviews"].replace(0, pd.NA)
    out["positive_ratio"] = out["positive_ratio"].fillna(0)

    out["review_signal"] = pd.cut(
        out["total_reviews"],
        bins=[-0.1, 0, 19, 99, 999, float("inf")],
        labels=["no_signal", "very_low", "low", "medium", "high"],
    )

    out["review_sentiment"] = pd.cut(
        out["positive_ratio"],
        bins=[-0.01, 0.4, 0.7, 1.0],
        labels=["weak", "mixed", "strong"],
    )

    out["price_bucket"] = pd.cut(
        out["Price"].fillna(0),
        bins=[-0.01, 0, 9.99, 29.99, 59.99, float("inf")],
        labels=["free", "budget", "mid", "premium", "luxury"],
    )

    out["platform_count"] = out[["Windows", "Mac", "Linux"]].fillna(False).astype(bool).sum(axis=1)
    out["genre_count"] = out["Genres"].apply(_count_pipe_items)
    out["tag_count"] = out["Tags"].apply(_count_pipe_items)
    out["screenshot_count"] = out["Screenshots"].apply(_count_pipe_items)
    out["movie_count"] = out["Movies"].apply(_count_pipe_items)

    return out
