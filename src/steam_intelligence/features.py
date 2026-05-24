"""Feature engineering helpers for Steam market analytics."""

from __future__ import annotations

import re

import numpy as np
import pandas as pd


def _to_numeric(series: pd.Series, default: float = np.nan) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip()
        .replace({"": np.nan, "none": np.nan, "nan": np.nan, "null": np.nan})
    )
    numeric = pd.to_numeric(cleaned, errors="coerce")
    if np.isnan(default):
        return numeric
    return numeric.fillna(default)


def _to_bool(value: object) -> bool:
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() in {"true", "1", "yes", "y", "t"}


def _split_owner_range(value: object) -> tuple[float, float]:
    """Split owner range strings like '20,000 - 50,000' into numeric bounds."""
    if pd.isna(value):
        return float("nan"), float("nan")

    text = str(value)
    nums = re.findall(r"\d[\d,]*", text)
    if len(nums) < 2:
        return float("nan"), float("nan")

    low = pd.to_numeric(nums[0].replace(",", ""), errors="coerce")
    high = pd.to_numeric(nums[1].replace(",", ""), errors="coerce")
    if pd.isna(low) or pd.isna(high):
        return float("nan"), float("nan")
    if low > high:
        low, high = high, low
    return float(low), float(high)


def _count_pipe_items(value: str) -> int:
    """Count list-like values separated by ';' or ',' in a robust way."""
    if pd.isna(value) or str(value).strip() == "":
        return 0

    text = str(value)
    sep = ";" if ";" in text else ","
    items = [item.strip() for item in text.split(sep) if item.strip()]
    return len(items)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create engineered features required for dashboard analytics."""
    out = df.copy()

    out["release_year"] = pd.to_datetime(out.get("Release date"), errors="coerce").dt.year

    owner_bounds = out.get("Estimated owners", pd.Series(index=out.index, dtype=object)).apply(_split_owner_range)
    out["owners_low"] = owner_bounds.apply(lambda x: x[0])
    out["owners_high"] = owner_bounds.apply(lambda x: x[1])
    out["owners_mid"] = (out["owners_low"] + out["owners_high"]) / 2

    positive = _to_numeric(out.get("Positive", pd.Series(0, index=out.index)), default=0).clip(lower=0)
    negative = _to_numeric(out.get("Negative", pd.Series(0, index=out.index)), default=0).clip(lower=0)
    out["total_reviews"] = positive + negative
    out["positive_rate"] = (positive / out["total_reviews"].replace(0, np.nan)).fillna(0)
    out["positive_ratio"] = out["positive_rate"]
    out["review_log"] = np.log1p(out["total_reviews"]).fillna(0)

    out["review_signal"] = pd.cut(
        out["total_reviews"],
        bins=[-0.1, 0, 19, 99, 999, float("inf")],
        labels=["no_signal", "very_low", "low", "medium", "high"],
    )

    out["review_sentiment"] = pd.cut(
        out["positive_rate"],
        bins=[-0.01, 0.4, 0.7, 1.0],
        labels=["weak", "mixed", "strong"],
    )

    price = _to_numeric(out.get("Price", pd.Series(0, index=out.index)), default=0).clip(lower=0)
    discount = _to_numeric(out.get("Discount", pd.Series(0, index=out.index)), default=0).clip(lower=0)
    out["is_free"] = price.eq(0)
    out["has_discount"] = discount.gt(0)

    out["price_bucket"] = pd.cut(
        price,
        bins=[-0.01, 0, 9.99, 29.99, 59.99, float("inf")],
        labels=["Free", "Low", "Medium", "High", "Premium"],
    )

    platforms = pd.DataFrame({
        "Windows": out.get("Windows", False),
        "Mac": out.get("Mac", False),
        "Linux": out.get("Linux", False),
    })
    out["platform_count"] = platforms.apply(lambda col: col.map(_to_bool)).sum(axis=1)
    out["genre_count"] = out.get("Genres", pd.Series(index=out.index, dtype=object)).apply(_count_pipe_items)
    out["tag_count"] = out.get("Tags", pd.Series(index=out.index, dtype=object)).apply(_count_pipe_items)
    out["screenshot_count"] = out.get("Screenshots", pd.Series(index=out.index, dtype=object)).apply(_count_pipe_items)
    out["movie_count"] = out.get("Movies", pd.Series(index=out.index, dtype=object)).apply(_count_pipe_items)

    return out
