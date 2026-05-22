# steam-game-intelligence-engine (V0.1)

A reproducible analytics project for understanding the Steam games market using a cleaning pipeline and Streamlit dashboard.

## Project structure
- `data/` - raw, sample, and processed datasets (large files ignored in git)
- `docs/` - documentation and data dictionary
- `reports/` - validation and quality report templates
- `notebooks/` - exploratory and audit notebooks
- `src/` - reusable Python package code
- `scripts/` - CLI utilities for pipeline and validation
- `app/` - Streamlit multi-page dashboard
- `tests/` - unit tests for core transformations

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
export PYTHONPATH=src
```

## Usage
```bash
PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned_sample.csv
PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned_sample.csv
streamlit run app/Home.py
```

If `data/processed/steam_games_cleaned.csv` is missing, the dashboard will fallback to `data/processed/steam_games_cleaned_sample.csv`.

## V0.1 engineered features
- `release_year`
- `owners_low`, `owners_high`, `owners_mid`
- `total_reviews`, `positive_ratio`
- `review_signal` (volume-based)
- `review_sentiment` (ratio-based)
- `price_bucket`
- `platform_count`
- `genre_count`, `tag_count`
- `screenshot_count`, `movie_count`
