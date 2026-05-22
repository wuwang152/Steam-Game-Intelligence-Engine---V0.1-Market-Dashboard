"""CLI entrypoint for the V0.1 cleaning pipeline."""

from steam_intelligence.cleaning import run_cleaning_pipeline


if __name__ == "__main__":
    df = run_cleaning_pipeline()
    print(f"Pipeline finished. Rows: {len(df):,} | Columns: {len(df.columns)}")
