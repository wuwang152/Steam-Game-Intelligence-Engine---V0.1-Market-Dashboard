# Changelog

All notable changes to this project are documented in this file.

## [0.2.0-unreleased] - 2026-05-24
### Added
- V0.2 analytical feature foundation kickoff with robust feature-engineering fields for market insights, including has_reviews.
- V0.2 Step 2 Market Insights Streamlit page (`app/pages/7_Market_Insights.py`) with V0.2 feature-aware filtering, KPI cards, market charts, scatter analysis, and top-game tables.
- V0.2 roadmap document (`docs/v0.2_roadmap.md`).
- V0.2 Step 4 reproducible Market Insights report generation script (`scripts/generate_market_report.py`) and report artifact output (`reports/steam_market_insights_v0.2.md`).

### Improved
- V0.2 Step 3 lightweight Market Insights visualization polish with clearer sectioning, filter summary, KPI formatting, chart grouping tabs, and ranking/hidden-gem presentation updates.
- Validation checks expanded for V0.2 analytical columns and value constraints.
- Test coverage expanded for mixed-type, missing-value, and edge-case feature engineering inputs.

## [0.1.0] - 2026-05-23
### Added
- Reproducible Steam data cleaning and feature-engineering pipeline.
- Validation script for processed output schema and data-quality checks.
- Pytest coverage for feature-engineering behavior and edge cases.
- GitHub Actions CI for automated repository checks.
- Multi-page Streamlit dashboard for market exploration.
- Dashboard screenshots in README (`docs/assets/dashboard_home.png`, `docs/assets/dashboard_attention.png`, `docs/assets/dashboard_genre_tag.png`).
- Support for full raw datasets placed under `data/raw/`.

### Improved
- Home dashboard visibility improvements, including column alias handling, readable price buckets, and compact preview table behavior.

### Notes
- Large raw datasets should remain under `data/raw/` and should not be committed.
