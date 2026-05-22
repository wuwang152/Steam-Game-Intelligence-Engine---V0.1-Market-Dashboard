"""Data cleaning pipeline for Steam dataset."""

from __future__ import annotations

import pandas as pd

from .config import PROCESSED_DATA_PATH, RAW_DATA_PATH
from .features import add_engineered_features

NUMERIC_COLS = [
    "Peak CCU", "Required age", "Price", "Discount", "DLC count", "Metacritic score",
    "User score", "Positive", "Negative", "Achievements", "Recommendations",
    "Average playtime forever", "Median playtime forever",
]


def clean_raw_steam_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize raw columns and parse types."""
    out = df.copy()
    out.columns = [col.strip() for col in out.columns]

    for col in NUMERIC_COLS:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    for col in ["Windows", "Mac", "Linux"]:
        if col in out.columns:
            out[col] = out[col].astype(str).str.lower().isin(["true", "1", "yes"])

    if "Name" in out.columns:
        out = out[out["Name"].notna() & (out["Name"].str.strip() != "")]

    return out


def run_cleaning_pipeline(input_path=RAW_DATA_PATH, output_path=PROCESSED_DATA_PATH) -> pd.DataFrame:
    """Load raw data, clean, engineer features, and save output."""
    df = pd.read_csv(input_path)
    cleaned = clean_raw_steam_data(df)
    featured = add_engineered_features(cleaned)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(output_path, index=False)
    return featured
