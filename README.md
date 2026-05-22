# steam-game-intelligence-engine (V0.1)

A serious, reproducible analytics project for understanding the Steam games market using a large public dataset and a Streamlit dashboard.

## Project goals
- Build a **reproducible cleaning pipeline** for raw Steam game data.
- Add **market-focused engineered features** for trend and segmentation analysis.
- Publish a **Streamlit dashboard** to explore release patterns, attention, pricing, and reputation.

## Project structure
- `data/` - raw and processed datasets (raw large files are ignored in git)
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
pip install pandas streamlit pytest
export PYTHONPATH=src
```

## Usage
1. Place raw CSV at: `data/raw/steam_games.csv`
2. Run cleaning + feature pipeline:
   ```bash
   PYTHONPATH=src python scripts/run_pipeline.py
   ```
3. Validate processed data:
   ```bash
   PYTHONPATH=src python scripts/validate_data.py
   ```
4. Launch dashboard:
   ```bash
   streamlit run app/Home.py
   ```
5. Open notebook `notebooks/01_data_audit.ipynb` for initial data audit.

## V0.1 engineered features
- `release_year`
- `owners_low`, `owners_high`, `owners_mid`
- `total_reviews`, `positive_ratio`, `review_signal`
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

## Limitations
- V0.1 uses simple parsing heuristics for list-like text columns.
- Owner ranges are midpoint approximations.
- No external enrichment (e.g., region pricing, seasonal trends) yet.

## Roadmap
- Add richer anomaly detection and schema contracts.
- Add cohort analyses (launch windows, franchise effects).
- Add forecasting slices and portfolio benchmarks.
- Add CI pipeline for automated testing and validation.
