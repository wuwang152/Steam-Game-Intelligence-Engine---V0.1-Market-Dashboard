"""Basic data quality validation checks for processed Steam dataset."""

from __future__ import annotations

import sys
import pandas as pd
from steam_intelligence.config import PROCESSED_DATA_PATH


def run_checks(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    required = ["AppID", "Name", "release_year", "Price", "positive_ratio", "owners_low", "owners_high"]
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


if __name__ == "__main__":
    df = pd.read_csv(PROCESSED_DATA_PATH)
    failures = run_checks(df)
    if failures:
        print("Validation failed:")
        for issue in failures:
            print(f"- {issue}")
        sys.exit(1)
    print("Validation passed.")
