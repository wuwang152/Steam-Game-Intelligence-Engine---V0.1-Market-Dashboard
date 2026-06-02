# Data Source Map (V0.3 Planning)

This document defines the source-to-dashboard mapping for the V0.3 planning layer and clarifies which files are local-only artifacts.

## Three-layer data system

1. **Raw dataset layer (local only)**
   - `data/raw/steam_games.csv`
   - Source file is large (~389MB) and should remain local.
   - It is intentionally excluded from GitHub commits.

2. **Processed and aggregation layer (local generated artifacts)**
   - Cleaned dataset: `data/processed/steam_games_cleaned.csv`
   - Dashboard aggregation tables: `data/processed/dashboard_tables/*.csv`
   - Aggregation tables are generated locally via:
     - `scripts/generate_dashboard_tables.py`

3. **Presentation layer**
   - Streamlit pages under `app/` and `app/pages/`
   - Markdown reports under `reports/`
   - Explanatory figures and visual assets under `docs/assets/`

## Dataset and artifact mapping

| Artifact type | Path | Source mode | Notes |
|---|---|---|---|
| Raw Steam dataset | `data/raw/steam_games.csv` | Local only | Not committed to GitHub |
| Cleaned dataset | `data/processed/steam_games_cleaned.csv` | Generated locally | Pipeline output |
| Dashboard aggregation tables | `data/processed/dashboard_tables/*.csv` | Generated locally | Built by `scripts/generate_dashboard_tables.py` |
| Reports and visual assets | `reports/`, `docs/assets/` | Versioned docs assets | Used for explanation and presentation |

## Page-level table mapping

| Page | Required backend tables / assets |
|---|---|
| Home | `summary_metrics` + `docs/assets/system_flow.svg` |
| 市场结构 | `yearly_release_counts`, `price_bucket_distribution`, `owners_tier_distribution`, `platform_count_distribution` + `docs/assets/market_structure_framework.png` |
| 口碑与热度 | `review_signal_distribution`, `review_sentiment_distribution`, `review_bucket_positive_rate`, `top_games_by_reviews`, `top_rated_games` + `docs/assets/reputation_attention_logic.png` |
| 赛道与本地化 | `genre_distribution`, `tag_distribution`, `category_distribution`, `language_support_summary`, `localization_by_genre` + `docs/assets/localization_framework.png` |
| 机会识别 | `hidden_gems`, `low_price_high_rating`, `high_attention_low_rating`, `chinese_supported_potential`, `localization_opportunities` + `docs/assets/opportunity_logic.png` |
| 后端聚合表预览 | all files in `dashboard_tables/*.csv` |

## Data safety policy

- Do not commit raw datasets from `data/raw/`.
- Do not commit generated outputs from `data/processed/`.
- Do not commit generated dashboard CSV tables.
