# v0.1.0 — Reproducible Steam Market Dashboard

## Summary
Version 0.1.0 establishes a reproducible baseline for Steam market analytics. The release combines a deterministic cleaning and feature-engineering pipeline with a multi-page Streamlit dashboard for descriptive exploration.

## Highlights
- Reproducible cleaning and feature-engineering pipeline.
- Validation workflow for processed output checks.
- Pytest coverage for feature engineering logic.
- GitHub Actions CI for automated checks.
- Multi-page Streamlit dashboard for market analysis.
- Dashboard screenshots documented in the README.
- Home dashboard visibility fixes (column aliases, readable price buckets, compact table preview).
- Support for full raw datasets placed under `data/raw/`.

## How to run locally
```bash
python -m pip install -r requirements.txt
PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned.csv
PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
PYTHONPATH=src pytest -q
PYTHONPATH=src streamlit run app/Home.py
```

## Dashboard pages
- `Home`
- `Overview`
- `Release Dynamics`
- `Attention Distribution`
- `Price and Monetization`
- `Reputation Signals`
- `Genre Tag Explorer`

## Known limitations
- Owner estimates are approximate because they are parsed from textual ranges.
- 2026 observations may represent partial-year data.
- V0.1 focuses on descriptive analytics, not recommendation or prediction.
- Full raw datasets should be placed under `data/raw/`, and large raw data should not be committed.

## Suggested V0.2 roadmap
- Improved dashboard interactivity.
- Large-dataset performance improvements.
- Better chart readability and outlier handling.
- Hidden-gem or market-opportunity scoring.
- Optional deployment to Streamlit Community Cloud.
- Possible recommendation or similarity-search module in later versions.
