# Steam Game Intelligence Engine (V0.1 Market Dashboard)

## Project overview
Steam Game Intelligence Engine V0.1 is a reproducible analytics project for Steam game-market exploration. It combines:

- a deterministic data cleaning and feature engineering pipeline, and
- a Streamlit dashboard for interactive market analysis.

The V0.1 release focuses on preprocessing reliability, feature consistency, and baseline dashboard usability. It is not yet a personalized recommendation system.

## Feature summary
- **Cleaning pipeline:** standardized typing, platform flag normalization, and row-level hygiene checks.
- **Engineered analytics features:** release timing, owner-range parsing, review ratios/signals, price segmentation, and metadata density counters.
- **Validation layer:** script-based checks for schema completeness and key data-quality constraints.
- **Automated tests:** unit tests covering feature-engineering behavior and edge-case handling.
- **Dashboard modules:** multi-page Streamlit interface for release, pricing, reputation, and genre/tag exploration.

## Repository structure
- `.github/workflows/` — CI workflow definitions.
- `app/` — Streamlit dashboard entrypoint and page modules.
- `data/raw/` — location for full raw datasets.
- `data/processed/` — generated cleaned/engineered outputs.
- `data/sample/` — reproducible sample datasets for demos and validation.
- `docs/` — project documentation and references.
- `notebooks/` — exploratory analysis notebooks.
- `reports/` — generated outputs and report artifacts.
- `scripts/` — operational CLI scripts for pipeline and validation.
- `src/steam_intelligence/` — core package logic.
- `tests/` — automated unit tests.

## Data usage and dataset placement
The included sample dataset is intended for reproducible demonstration and local validation:

- `data/sample/games_sample.csv`

For full-scale processing, place raw datasets under:

- `data/raw/`

Example conventional path:

- `data/raw/steam_games.csv`

## Quick start
### 1) Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 2) Run pipeline with sample data
```bash
PYTHONPATH=src python scripts/run_pipeline.py --input data/sample/games_sample.csv --output data/processed/steam_games_cleaned.csv
```

### 3) Validate processed output
```bash
PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
```

### 4) Run tests
```bash
PYTHONPATH=src pytest -q
```

### 5) Launch dashboard
```bash
PYTHONPATH=src streamlit run app/Home.py
```

## Dashboard overview
V0.1 dashboard modules:

- `app/Home.py`
- `app/pages/1_Overview.py`
- `app/pages/2_Release_Dynamics.py`
- `app/pages/3_Attention_Distribution.py`
- `app/pages/4_Price_and_Monetization.py`
- `app/pages/5_Reputation_Signals.py`
- `app/pages/6_Genre_Tag_Explorer.py`

These modules provide baseline market exploration views for pricing, release cadence, review activity, and genre/tag distribution.

## Testing and CI
### Local testing
Use the same project commands for local validation:

```bash
PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
PYTHONPATH=src pytest -q
```

### Continuous Integration
GitHub Actions is configured to run repository checks on pushes and pull requests, including dependency installation and automated test/validation steps.

## Limitations
- Owner ranges are inferred from string intervals and remain approximate.
- Transformations are rules-based and intentionally lightweight for V0.1.
- Dashboard capabilities are baseline and focused on descriptive exploration.
- V0.1 does not yet implement recommendation or ranking personalization.

## Roadmap
- Expand data-quality validations and edge-case guardrails.
- Improve dashboard interactivity and comparative slicing.
- Scale workflows for full raw datasets placed under `data/raw/`.
- Add additional market signals and higher-level composite indicators.
- Increase automated test coverage across pipeline stages.

## Dashboard screenshots (placeholder)
Screenshots will be added in a future update after dedicated dashboard visual QA and capture.
