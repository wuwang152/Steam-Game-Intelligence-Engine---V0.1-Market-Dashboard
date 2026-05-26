# System Architecture (V0.3 Planning)

## Overview

The dashboard is organized as a three-layer pipeline to keep data handling reproducible and the UI responsive:

1. Raw source dataset (`data/raw/steam_games.csv`, local only)
2. Cleaned and standardized dataset (`data/processed/steam_games_cleaned.csv`)
3. Dashboard-ready aggregation tables (`data/processed/dashboard_tables/*.csv`) consumed by Streamlit pages

## Data flow

1. **Raw ingest**
   - Full Steam dataset is stored locally under `data/raw/`.

2. **Cleaning and feature engineering**
   - Pipeline scripts convert raw records into a cleaned analytical table.

3. **Dashboard aggregation generation**
   - `scripts/generate_dashboard_tables.py` materializes page-specific summary CSV tables.

4. **Presentation consumption**
   - Streamlit pages read the pre-aggregated tables for rendering.
   - Documentation and presentation assets live in `reports/` and `docs/assets/`.

## Why frontend should prefer backend aggregation tables

- **Speed:** pre-aggregated CSV tables reduce in-page compute and improve load times.
- **Stability:** each page reads bounded, schema-consistent outputs rather than re-running heavy transformations.
- **Consistency:** all pages use the same generated metrics definitions, reducing drift.
- **Operational clarity:** aggregation scripts become the single source of truth for dashboard metrics.

## Why raw data is local and excluded from GitHub

- The raw dataset is large (about 389MB), making repository history heavy and inefficient.
- Local-only raw data keeps version control focused on code and documentation rather than bulky artifacts.
- Generated processed outputs can be recreated via project scripts, so reproducibility is preserved without committing large data files.
