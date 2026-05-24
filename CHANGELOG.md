# Changelog

All notable changes to this project are documented in this file.

## [0.2.0] - 2026-05-24
### Added
- V0.2 analytical feature engineering foundation with robust market-insights fields, including `has_reviews`.
- V0.2 Market Insights Streamlit page (`app/pages/7_Market_Insights.py`) with V0.2 feature-aware filtering, KPI cards, market charts, scatter analysis, and top-game tables.
- V0.2 reproducible Market Insights report generation script (`scripts/generate_market_report.py`) and report artifact output (`reports/steam_market_insights_v0.2.md`).
- V0.2 roadmap document (`docs/v0.2_roadmap.md`).

### Improved
- Dashboard readability and terminology consistency: clearer sectioning, filter summary, KPI formatting, stable category ordering, readable ownership-tier view, and concise interpretation notes across key pages.
- Validation checks expanded for V0.2 analytical columns and value constraints.
- Test coverage expanded for mixed-type, missing-value, and edge-case feature-engineering inputs.
- README and project presentation cleanup with V0.2 positioning, report linkage, cross-platform command examples, and clarified interpretation notes.

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
