"""CLI entrypoint for the V0.1 cleaning pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from steam_intelligence.cleaning import run_cleaning_pipeline
from steam_intelligence.config import PROCESSED_DATA_PATH, RAW_DATA_PATH


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Steam cleaning + feature pipeline")
    parser.add_argument("--input", type=Path, default=RAW_DATA_PATH, help="Path to raw input CSV")
    parser.add_argument("--output", type=Path, default=PROCESSED_DATA_PATH, help="Path to output CSV")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    df = run_cleaning_pipeline(input_path=args.input, output_path=args.output)
    print(f"Pipeline finished. Rows: {len(df):,} | Columns: {len(df.columns)}")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
