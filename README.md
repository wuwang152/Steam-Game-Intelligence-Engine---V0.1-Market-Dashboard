# Steam Game Intelligence Engine (V0.1 Market Dashboard)

## Project overview
Steam Game Intelligence Engine (V0.1 Market Dashboard) is a reproducible Steam games data project that combines:
- a data cleaning and feature engineering pipeline, and
- a Streamlit dashboard for market-oriented exploration.

V0.1 is focused on reliable preprocessing, validation, and a basic dashboard experience. It is **not** yet a full personalized recommendation system.

## Current V0.1 status
The current project includes:
- sample dataset for local testing
- cleaning pipeline
- feature engineering
- validation script
- environment check script
- Streamlit dashboard scaffold
- GitHub Actions CI
- local setup guide

## Project structure
- `.github/workflows/` - CI workflows for automated validation on pushes and pull requests.
- `app/` - Streamlit dashboard entrypoint and pages.
- `data/raw/` - location for large raw source data files (not committed when large).
- `data/processed/` - generated cleaned/engineered outputs.
- `data/sample/` - lightweight sample datasets for quick local validation and demos.
- `docs/` - supporting documentation and notes.
- `notebooks/` - exploratory notebooks.
- `reports/` - generated reports and output artifacts.
- `scripts/` - operational scripts (environment checks, pipeline run, data validation).
- `src/steam_intelligence/` - core package code for transformations and feature logic.
- `tests/` - automated tests.
- `AGENTS.md` - Codex environment and validation command guidance.
- `LOCAL_SETUP.md` - detailed local setup and run instructions.
- `requirements.txt` - Python dependency list.

## Dataset
The full raw Steam dataset is not committed because it is large.

Place the full raw CSV at:
- `data/raw/steam_games.csv`

For local testing and demonstration, use:
- `data/sample/games_sample.csv`

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Windows PowerShell setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
```

## Quick start with sample data
```bash
PYTHONPATH=src python scripts/check_environment.py
PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned.csv
PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
PYTHONPATH=src pytest -q
PYTHONPATH=src streamlit run app/Home.py
```

## Windows PowerShell quick start
```powershell
$env:PYTHONPATH = "src"
python scripts/check_environment.py
python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned.csv
python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
pytest -q
streamlit run app/Home.py
```

## Engineered features
- `release_year`
- `owners_low`
- `owners_high`
- `owners_mid`
- `total_reviews`
- `positive_ratio`
- `review_signal`
- `review_sentiment`
- `price_bucket`
- `platform_count`
- `genre_count`
- `tag_count`
- `screenshot_count`
- `movie_count`

## Validation and CI
GitHub Actions runs dependency installation, environment checks, sample pipeline execution, data validation, and `pytest` on pull requests and pushes to `main`.

`scripts/check_environment.py` verifies that `pandas`, `numpy`, `streamlit`, and `pytest` are installed.

## Data handling rules
- Do not commit large raw datasets.
- Keep raw source data under `data/raw/`.
- Keep generated processed outputs under `data/processed/`.
- Use sample data for testing and demos.

## Limitations
- Owner ranges are approximations.
- V0.1 uses simple parsing rules.
- Dashboard pages are initial scaffolds.
- This is not yet a personalized recommendation system.

## Roadmap
- improve tests
- improve dashboard charts
- adapt to full Kaggle dataset
- add Hidden Gem Score
- add tag/genre analysis
- add text similarity search later
