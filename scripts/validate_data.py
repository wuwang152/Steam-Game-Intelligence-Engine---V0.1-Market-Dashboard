"""Basic data quality validation checks for processed Steam dataset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


def run_checks(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    required = [
        "AppID", "Name", "release_year", "Price", "positive_ratio",
        "owners_low", "owners_high", "review_signal", "review_sentiment",
    ]
    missing_cols = [col for col in required if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        return errors

    if df["AppID"].isna().any():
        errors.append("AppID has missing values")
    if df["AppID"].duplicated().any():
        errors.append("AppID contains duplicates")
    if (df["Price"].fillna(0) < 0).any():
        errors.append("Price contains negative values")
    if ((df["positive_ratio"] < 0) | (df["positive_ratio"] > 1)).any():
        errors.append("positive_ratio must be in [0, 1]")
    if (df["owners_low"] > df["owners_high"]).any():
        errors.append("owners_low cannot exceed owners_high")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate cleaned Steam dataset.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV file.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. Run the pipeline first or pass a valid --input path."
        )

    df = pd.read_csv(input_path)
    failures = run_checks(df)
    if failures:
        print("Validation failed:")
        for issue in failures:
            print(f"- {issue}")
        sys.exit(1)
    print("Validation passed.")
