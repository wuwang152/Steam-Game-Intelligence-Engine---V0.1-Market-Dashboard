from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from steam_intelligence.dashboard_tables import build_dashboard_tables, write_dashboard_tables


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate dashboard aggregation tables")
    parser.add_argument("--input", type=Path, default=Path("data/processed/steam_games_cleaned.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/dashboard_tables"))
    parser.add_argument("--top-n", type=int, default=30)
    parser.add_argument("--min-reviews", type=int, default=20)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    df = pd.read_csv(args.input)
    tables = build_dashboard_tables(df, top_n=args.top_n, min_reviews=args.min_reviews)
    write_dashboard_tables(tables, args.output_dir)
    print(f"Generated {len(tables)} tables in {args.output_dir}")
