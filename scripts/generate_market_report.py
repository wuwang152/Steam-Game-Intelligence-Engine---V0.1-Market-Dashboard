#!/usr/bin/env python
"""Generate reproducible Steam market insights markdown report."""

from __future__ import annotations

import argparse
import sys

import pandas as pd

from steam_intelligence.reporting import render_report, validate_required_columns, write_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Steam market insights markdown report")
    parser.add_argument("--input", default="data/processed/steam_games_cleaned.csv", help="Path to processed CSV")
    parser.add_argument("--output", default="reports/steam_market_insights_v0.2.md", help="Path to output markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        df = pd.read_csv(args.input)
    except FileNotFoundError:
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        return 1

    missing = validate_required_columns(df)
    if missing:
        print(
            "Error: input dataset is missing required V0.2 columns: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 1

    report_md = render_report(df, args.input)
    write_report(report_md, args.output)
    print(f"Report generated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
