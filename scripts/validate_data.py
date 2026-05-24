"""Basic data quality validation checks for processed Steam dataset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from steam_intelligence.config import PROCESSED_DATA_PATH


REQUIRED_COLUMNS = [
    "AppID",
    "Name",
    "Price",
    "release_year",
    "owners_low",
    "owners_high",
    "owners_mid",
    "total_reviews",
    "positive_rate",
    "review_log",
    "is_free",
    "has_discount",
    "platform_count",
    "price_bucket",
]


def run_checks(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        return errors

    if df["AppID"].isna().any():
        errors.append("AppID has missing values")

    if df["AppID"].duplicated().any():
        errors.append("AppID contains duplicates")

    if (df["Price"].fillna(0) < 0).any():
        errors.append("Price contains negative values")

    if (df["total_reviews"].fillna(0) < 0).any():
        errors.append("total_reviews must be non-negative")

    rate = df["positive_rate"].dropna()
    if ((rate < 0) | (rate > 1)).any():
        errors.append("positive_rate must be in [0, 1] where non-null")

    if (df["review_log"].fillna(0) < 0).any():
        errors.append("review_log must be non-negative")

    pc = df["platform_count"].dropna()
    if ((pc < 0) | (pc > 3)).any():
        errors.append("platform_count must be in [0, 3]")

    owners_mid = df["owners_mid"].dropna()
    if (owners_mid < 0).any():
        errors.append("owners_mid must be non-negative where non-null")

    years = df["release_year"].dropna()
    if ((years < 1980) | (years > 2100)).any():
        errors.append("release_year must be in a reasonable range [1980, 2100] where non-null")

    if (df["owners_low"] > df["owners_high"]).any():
        errors.append("owners_low cannot exceed owners_high")

    if len(df) == 0:
        errors.append("Processed dataset is empty")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate processed Steam dataset")
    parser.add_argument("--input", type=Path, default=PROCESSED_DATA_PATH, help="Path to processed CSV")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    df = pd.read_csv(args.input)
    failures = run_checks(df)
    if failures:
        print("Validation failed:")
        for issue in failures:
            print(f"- {issue}")
        sys.exit(1)
    print("Validation passed.")
