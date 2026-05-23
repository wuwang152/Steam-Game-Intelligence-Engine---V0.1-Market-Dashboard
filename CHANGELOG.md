# Changelog

All notable changes to this project are documented in this file.

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
