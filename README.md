# steam-game-intelligence-engine (V0.1)

A serious, reproducible analytics project for understanding the Steam games market using a large public dataset and a Streamlit dashboard.

## Project goals
- Build a **reproducible cleaning pipeline** for raw Steam game data.
- Add **market-focused engineered features** for trend and segmentation analysis.
- Publish a **Streamlit dashboard** to explore release patterns, attention, pricing, and reputation.

## Project structure
- `data/` - raw and processed datasets (large raw source files should not be committed to git)
- `docs/` - documentation and design notes
- `reports/` - exported analysis outputs and summaries
- `notebooks/` - exploratory and audit notebooks
- `src/` - reusable Python package code
- `scripts/` - CLI utilities for pipeline and validation
- `app/` - Streamlit multi-page dashboard
- `tests/` - unit tests for core transformations

## Dataset schema (raw)
Expected raw columns include:
`AppID, Name, Release date, Estimated owners, Peak CCU, Required age, Price, Discount, DLC count, About the game, Supported languages, Full audio languages, Windows, Mac, Linux, Metacritic score, User score, Positive, Negative, Achievements, Recommendations, Average playtime forever, Median playtime forever, Developers, Publishers, Categories, Genres, Tags, Screenshots, Movies`.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Usage (sample dataset)
```bash
PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned.csv
PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
PYTHONPATH=src pytest -q
streamlit run app/Home.py
```

## Usage (Windows PowerShell)
```powershell
$env:PYTHONPATH="src"
python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned.csv
python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
pytest -q
streamlit run app/Home.py
```

## V0.1 engineered features
- `release_year`
- `owners_low`, `owners_high`, `owners_mid`
- `total_reviews`, `positive_ratio`, `review_signal`, `review_sentiment`
- `price_bucket`
- `platform_count`
- `genre_count`, `tag_count`
- `screenshot_count`, `movie_count`

## Validation rules (V0.1)
- Required columns exist.
- `AppID` has no missing or duplicate values.
- `Price >= 0`.
- `positive_ratio` is in `[0, 1]`.
- `owners_low <= owners_high`.

## Data handling note
- Do not commit large raw datasets to git; keep them local (for example under `data/raw/`) and only commit small synthetic/sample files needed for reproducible examples.

## Limitations
- V0.1 uses simple parsing heuristics for list-like text columns.
- Owner ranges are midpoint approximations.
- No external enrichment (e.g., region pricing, seasonal trends) yet.

## Roadmap
- Add richer anomaly detection and schema contracts.
- Add cohort analyses (launch windows, franchise effects).
- Add forecasting slices and portfolio benchmarks.
- Add CI pipeline for automated testing and validation.
