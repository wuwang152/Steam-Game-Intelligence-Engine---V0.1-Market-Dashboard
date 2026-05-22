"""CLI entrypoint for the V0.1 cleaning pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from steam_intelligence.cleaning import run_cleaning_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Steam data cleaning pipeline.")
    parser.add_argument("--input", required=True, help="Path to raw input CSV.")
    parser.add_argument("--output", required=True, help="Path for cleaned output CSV.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. Please provide a valid CSV using --input."
        )

    df = run_cleaning_pipeline(input_path=input_path, output_path=output_path)
    print(f"Pipeline finished. Rows: {len(df):,} | Columns: {len(df.columns)} | Output: {output_path}")
