# Steam Market Insights Report V0.2

## 1. Project Overview
This report summarizes descriptive V0.2 market analytics for the Steam Game Intelligence Engine.

## 2. Data and Analytical Features
The metrics in this document are computed from the available processed dataset file: `data/processed/steam_games_cleaned.csv`.
Required V0.2 analytical fields include release, ownership proxy, review, pricing, and platform features.

## 3. Executive Summary
- Total games: **5**
- Games with reviews: **5** (100.0%)
- Median owners_mid (estimated ownership proxy): **35,000**
- Median total_reviews: **7,000**
- Median positive_rate among reviewed games: **83.3%**
- Free game share: **20.0%**
- Discounted game share: **40.0%**

## 4. Market Structure
- Release year range: **2,017 to 2,023**
- Top release years by game count:
- 2021: 1 games
- 2019: 1 games
- 2023: 1 games
- 2017: 1 games
- 2020: 1 games

### Price Bucket Distribution
| price_bucket | Count | Share |
| --- | --- | --- |
| mid | 3 | 60.0% |
| budget | 1 | 20.0% |
| free | 1 | 20.0% |

### Platform Count Distribution
| platform_count | Count | Share |
| --- | --- | --- |
| 1 | 2 | 40.0% |
| 3 | 2 | 40.0% |
| 2 | 1 | 20.0% |

### Review Signal Distribution
| review_signal | Count | Share |
| --- | --- | --- |
| high | 5 | 100.0% |

## 5. Pricing and Monetization
Pricing structure is described with `price_bucket`, `is_free`, and `has_discount` metrics from the available processed dataset.

## 6. Review and Popularity Signals
`positive_rate` is most meaningful for games with reviews. `review_log` and `total_reviews` are descriptive popularity proxies.

### Review Sentiment Distribution
| review_sentiment | Count | Share |
| --- | --- | --- |
| strong | 5 | 100.0% |

## 7. Top Games and Hidden Gems
### Top 10 Games by owners_mid
| Name | release_year | price_bucket | owners_mid | total_reviews | positive_rate | platform_count | Genres | Tags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Retro Kart Arena | 2,017 | mid | 150,000 | 24,000 | 75.0% | 1 | Racing;Multiplayer | Arcade;Party;Local Multiplayer |
| Dungeon Sprint | 2,019 | budget | 75,000 | 15,000 | 83.3% | 1 | Action;Roguelike | Indie;Fast-Paced;Difficult |
| Galaxy Traders | 2,021 | mid | 35,000 | 5,000 | 84.0% | 2 | Strategy;Simulation | Space;Trading;Singleplayer |
| Open Ocean Builder | 2,020 | free | 15,000 | 7,000 | 80.0% | 3 | Sandbox;Building | Crafting;Exploration;Indie |
| Cozy Garden VR | 2,023 | mid | 7,500 | 1,000 | 87.0% | 3 | Casual;Simulation | Relaxing;VR;Farming |

### Top 10 Games by total_reviews
| Name | release_year | price_bucket | owners_mid | total_reviews | positive_rate | platform_count | Genres | Tags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Retro Kart Arena | 2,017 | mid | 150,000 | 24,000 | 75.0% | 1 | Racing;Multiplayer | Arcade;Party;Local Multiplayer |
| Dungeon Sprint | 2,019 | budget | 75,000 | 15,000 | 83.3% | 1 | Action;Roguelike | Indie;Fast-Paced;Difficult |
| Open Ocean Builder | 2,020 | free | 15,000 | 7,000 | 80.0% | 3 | Sandbox;Building | Crafting;Exploration;Indie |
| Galaxy Traders | 2,021 | mid | 35,000 | 5,000 | 84.0% | 2 | Strategy;Simulation | Space;Trading;Singleplayer |
| Cozy Garden VR | 2,023 | mid | 7,500 | 1,000 | 87.0% | 3 | Casual;Simulation | Relaxing;VR;Farming |

### Top 10 Rated Games by positive_rate (minimum 7000 reviews)
| Name | release_year | price_bucket | owners_mid | total_reviews | positive_rate | platform_count | Genres | Tags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dungeon Sprint | 2,019 | budget | 75,000 | 15,000 | 83.3% | 1 | Action;Roguelike | Indie;Fast-Paced;Difficult |
| Open Ocean Builder | 2,020 | free | 15,000 | 7,000 | 80.0% | 3 | Sandbox;Building | Crafting;Exploration;Indie |
| Retro Kart Arena | 2,017 | mid | 150,000 | 24,000 | 75.0% | 1 | Racing;Multiplayer | Arcade;Party;Local Multiplayer |

### Potential Hidden Gems (Heuristic Candidates)
Heuristic only (not model predictions): positive_rate >= 85%, total_reviews >= 20, and owners_mid at or below candidate median.

| Name | release_year | price_bucket | owners_mid | total_reviews | positive_rate | platform_count | Genres | Tags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cozy Garden VR | 2,023 | mid | 7,500 | 1,000 | 87.0% | 3 | Casual;Simulation | Relaxing;VR;Farming |

## 8. Key Observations
In the available processed dataset, the market profile is summarized through descriptive distributions and ranking tables above.
These observations are descriptive and centered on estimated ownership proxy and review proxies.

## 9. Limitations
- `owners_mid` is an estimated midpoint of owner ranges, not exact sales.
- Estimated owners should not be interpreted as exact sales.
- Review counts and `positive_rate` are proxies for attention and reception.
- Dataset coverage depends on the raw source file.
- This V0.2 report is descriptive and does not include causal inference or machine learning predictions.

## 10. Next Steps
- Game segmentation
- Ranking score system
- Genre/tag opportunity analysis
- Predictive modeling later, after descriptive analysis is stable
