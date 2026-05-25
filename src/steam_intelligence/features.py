"""Feature engineering helpers for Steam market analytics."""

from __future__ import annotations

import re

import numpy as np
import pandas as pd


def _to_numeric(series: pd.Series, default: float = np.nan) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(r"[^0-9.\-]", "", regex=True)
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


MISSING_TEXT_TOKENS = {"", "none", "nan", "null", "n/a", "na", "[]", "-"}


def _is_missing_text(value: object) -> bool:
    if pd.isna(value):
        return True
    return str(value).strip().lower() in MISSING_TEXT_TOKENS


def _split_list_items(value: object) -> list[str]:
    if _is_missing_text(value):
        return []
    text = str(value).strip()
    return [item.strip() for item in re.split(r"[;,]", text) if not _is_missing_text(item)]


def _count_pipe_items(value: str) -> int:
    """Count list-like values separated by ';' or ',' in a robust way."""
    return len(_split_list_items(value))


def _is_nonempty_text(value: object) -> bool:
    return not _is_missing_text(value)


def _contains_language(value: object, patterns: tuple[str, ...], *, case_insensitive: bool = True) -> bool:
    if not _is_nonempty_text(value):
        return False
    text = str(value)
    haystack = text.lower() if case_insensitive else text
    needles = [p.lower() for p in patterns] if case_insensitive else list(patterns)
    return any(needle in haystack for needle in needles)


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
    out["has_reviews"] = out["total_reviews"] > 0
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
    out["review_sentiment"] = out["review_sentiment"].cat.add_categories(["no_reviews"])
    out.loc[~out["has_reviews"], "review_sentiment"] = "no_reviews"

    price = _to_numeric(out.get("Price", pd.Series(0, index=out.index)), default=0).clip(lower=0)
    discount = _to_numeric(out.get("Discount", pd.Series(0, index=out.index)), default=0).clip(lower=0)
    out["is_free"] = price.eq(0)
    out["has_discount"] = discount.gt(0)

    out["price_bucket"] = pd.cut(
        price,
        bins=[-0.01, 0, 9.99, 29.99, 59.99, float("inf")],
        labels=["free", "budget", "mid", "premium", "luxury"],
    )

    platforms = pd.DataFrame({
        "Windows": out.get("Windows", pd.Series(False, index=out.index)),
        "Mac": out.get("Mac", pd.Series(False, index=out.index)),
        "Linux": out.get("Linux", pd.Series(False, index=out.index)),
    })
    out["platform_count"] = platforms.apply(lambda col: col.map(_to_bool)).sum(axis=1)
    out["genre_count"] = out.get("Genres", pd.Series(index=out.index, dtype=object)).apply(_count_pipe_items)
    out["tag_count"] = out.get("Tags", pd.Series(index=out.index, dtype=object)).apply(_count_pipe_items)
    out["screenshot_count"] = out.get("Screenshots", pd.Series(index=out.index, dtype=object)).apply(_count_pipe_items)
    out["movie_count"] = out.get("Movies", pd.Series(index=out.index, dtype=object)).apply(_count_pipe_items)

    metascore = _to_numeric(out.get("Metacritic score", pd.Series(0, index=out.index)), default=0)
    user_score = _to_numeric(out.get("User score", pd.Series(0, index=out.index)), default=0)
    out["has_valid_metascore"] = metascore.gt(0)
    out["has_valid_user_score"] = user_score.gt(0)

    peak_ccu = _to_numeric(out.get("Peak CCU", pd.Series(0, index=out.index)), default=0)
    recommendations = _to_numeric(out.get("Recommendations", pd.Series(0, index=out.index)), default=0)
    avg_playtime_forever = _to_numeric(out.get("Average playtime forever", pd.Series(0, index=out.index)), default=0)
    median_playtime_forever = _to_numeric(out.get("Median playtime forever", pd.Series(0, index=out.index)), default=0)
    avg_playtime_2w = _to_numeric(out.get("Average playtime two weeks", pd.Series(0, index=out.index)), default=0)
    median_playtime_2w = _to_numeric(out.get("Median playtime two weeks", pd.Series(0, index=out.index)), default=0)

    out["has_peak_ccu"] = peak_ccu.gt(0)
    out["has_recommendations"] = recommendations.gt(0)
    out["has_playtime_forever"] = avg_playtime_forever.gt(0) | median_playtime_forever.gt(0)
    out["has_recent_playtime"] = avg_playtime_2w.gt(0) | median_playtime_2w.gt(0)

    out["has_genres"] = out.get("Genres", pd.Series(index=out.index, dtype=object)).map(_is_nonempty_text)
    out["has_tags"] = out.get("Tags", pd.Series(index=out.index, dtype=object)).map(_is_nonempty_text)
    out["has_categories"] = out.get("Categories", pd.Series(index=out.index, dtype=object)).map(_is_nonempty_text)
    out["has_developer"] = out.get("Developers", pd.Series(index=out.index, dtype=object)).map(_is_nonempty_text)
    out["has_publisher"] = out.get("Publishers", pd.Series(index=out.index, dtype=object)).map(_is_nonempty_text)
    out["has_header_image"] = out.get("Header image", pd.Series(index=out.index, dtype=object)).map(_is_nonempty_text)
    out["has_about_text"] = out.get("About the game", pd.Series(index=out.index, dtype=object)).map(_is_nonempty_text)
    out["has_screenshots"] = out["screenshot_count"].gt(0)

    supported_languages = out.get("Supported languages", pd.Series(index=out.index, dtype=object))
    full_audio_languages = out.get("Full audio languages", pd.Series(index=out.index, dtype=object))

    out["supported_language_count"] = supported_languages.map(_count_pipe_items)
    out["full_audio_language_count"] = full_audio_languages.map(_count_pipe_items)

    simplified_patterns = ("simplified chinese", "chinese (simplified)", "chinese - simplified", "simplified_chinese", "简体中文")
    out["supports_simplified_chinese"] = supported_languages.map(lambda v: _contains_language(v, simplified_patterns))
    out["supports_english"] = supported_languages.map(lambda v: _contains_language(v, ("english", "英语")))
    out["supports_japanese"] = supported_languages.map(lambda v: _contains_language(v, ("japanese", "日语", "日本語")))
    out["supports_korean"] = supported_languages.map(lambda v: _contains_language(v, ("korean", "韩语", "한국어")))
    out["has_chinese_audio"] = full_audio_languages.map(
        lambda v: _contains_language(v, simplified_patterns + ("chinese", "中文", "汉语", "漢語"))
    )

    return out
