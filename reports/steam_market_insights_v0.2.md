# Steam Market Insights Report V0.2

## 1. Project Overview
This report summarizes descriptive V0.2 market analytics for the Steam Game Intelligence Engine.

## 2. Data and Analytical Features
The metrics in this document are computed from the available processed dataset file: `data\processed\steam_games_cleaned.csv`.
Required V0.2 analytical fields include release, ownership proxy, review, pricing, and platform features.

## 3. Executive Summary
- Total games: **122,610**
- Games with reviews: **82,949** (67.7%)
- Median owners_mid (estimated ownership proxy): **10,000**
- Median total_reviews: **7**
- Median positive_rate among reviewed games: **81.8%**
- Free game share: **21.4%**
- Discounted game share: **33.2%**

## 4. Market Structure
- Release year range: **1,997 to 2,026**
- Top release years by game count:
- 2025: 24,973 games
- 2024: 20,031 games
- 2023: 14,596 games
- 2022: 12,284 games
- 2021: 11,067 games
- 2020: 8,804 games
- 2018: 7,461 games
- 2019: 7,242 games
- 2017: 5,920 games
- 2016: 4,140 games

### Price Bucket Distribution
| price_bucket | Count | Share |
| --- | --- | --- |
| budget | 84,605 | 69.0% |
| free | 26,205 | 21.4% |
| mid | 10,706 | 8.7% |
| premium | 699 | 0.6% |
| luxury | 395 | 0.3% |

### Platform Count Distribution
| platform_count | Count | Share |
| --- | --- | --- |
| 1 | 96,959 | 79.1% |
| 2 | 14,348 | 11.7% |
| 3 | 11,303 | 9.2% |

### Review Signal Distribution
| review_signal | Count | Share |
| --- | --- | --- |
| no_signal | 39,661 | 32.3% |
| very_low | 38,388 | 31.3% |
| low | 21,761 | 17.7% |
| medium | 15,594 | 12.7% |
| high | 7,206 | 5.9% |

## 5. Pricing and Monetization
Pricing structure is described with `price_bucket`, `is_free`, and `has_discount` metrics from the available processed dataset.

## 6. Review and Popularity Signals
`positive_rate` is most meaningful for games with reviews. `review_log` and `total_reviews` are descriptive popularity proxies.

### Review Sentiment Distribution
| review_sentiment | Count | Share |
| --- | --- | --- |
| strong | 56,464 | 46.1% |
| no_reviews | 39,661 | 32.3% |
| mixed | 19,190 | 15.7% |
| weak | 7,295 | 5.9% |

## 7. Top Games and Hidden Gems
### Top 10 Games by owners_mid
| Name | release_year | price_bucket | owners_mid | total_reviews | positive_rate | platform_count | Genres | Tags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Counter-Strike 2 | 2,012 | free | 150,000,000 | 8,815,087 | 86.7% | 2 | Action,Free To Play | FPS,Shooter,Multiplayer,Competitive,Action,Team-Based,e-sports,Tactical,First-Person,PvP,Online Co-Op,Co-op,Strategy,Military,War,Difficult,Trading,Realistic,Fast-Paced,Moddable |
| PUBG: BATTLEGROUNDS | 2,017 | free | 150,000,000 | 2,557,944 | 59.4% | 1 | Action,Adventure,Massively Multiplayer,Free To Play | Survival,Shooter,Battle Royale,Multiplayer,FPS,PvP,Third-Person Shooter,Action,Online Co-Op,Tactical,Co-op,First-Person,Strategy,Early Access,Competitive,Third Person,Team-Based,Difficult,Simulation,Stealth |
| Dota 2 | 2,013 | free | 150,000,000 | 2,498,969 | 81.5% | 3 | Action,Strategy,Free To Play | Free to Play,MOBA,Multiplayer,Strategy,e-sports,Team-Based,Competitive,Action,Online Co-Op,PvP,Difficult,Co-op,RTS,RPG,Tower Defense,Fantasy,Character Customization,Replay Value,Action RPG,Simulation |
| Apex Legends™ | 2,020 | free | 150,000,000 | 994,979 | 67.1% | 1 | Action,Adventure,Free To Play | Free to Play,Battle Royale,Multiplayer,FPS,Shooter,First-Person,PvP,Action,Hero Shooter,Team-Based,Tactical,Sci-fi,Loot,Survival,Co-op,Character Customization,Funny,Lore-Rich,Cyberpunk,Cinematic |
| Grand Theft Auto V Legacy | 2,015 | free | 75,000,000 | 1,990,556 | 87.4% | 1 | Action,Adventure | Open World,Action,Multiplayer,Crime,Automobile Sim,Third Person,First-Person,Mature,Shooter,Adventure,Singleplayer,Third-Person Shooter,Racing,Co-op,Sandbox,Atmospheric,Funny,Great Soundtrack,Comedy,Moddable |
| Team Fortress 2 | 2,007 | free | 75,000,000 | 1,161,472 | 89.9% | 2 | Action,Free To Play | Free to Play,Hero Shooter,Multiplayer,FPS,Shooter,Action,Class-Based,Team-Based,Funny,First-Person,Online Co-Op,Competitive,Cartoony,Trading,Co-op,Comedy,Robots,Tactical,Cartoon,Crafting |
| Black Myth: Wukong | 2,024 | premium | 75,000,000 | 1,150,098 | 96.7% | 1 | Action,Adventure,RPG | Mythology,Action RPG,Action,Souls-like,RPG,Combat,Story Rich,Singleplayer,Action-Adventure,Drama,Dark Fantasy,Atmospheric,Adventure,3D,Fantasy,Hack and Slash,Difficult,Third Person,Music,Violent |
| Left 4 Dead 2 | 2,009 | budget | 75,000,000 | 963,983 | 97.5% | 2 | Action | Zombies,Co-op,FPS,Multiplayer,Shooter,Online Co-Op,Action,Survival,Horror,First-Person,Gore,Team-Based,Moddable,Survival Horror,Post-apocalyptic,Singleplayer,Adventure,Local Co-Op,Replay Value,Tactical |
| Call of Duty® | 2,022 | free | 75,000,000 | 714,114 | 58.8% | 1 | Action | FPS,Multiplayer,Shooter,Singleplayer,Action,Military,First-Person,War,Modern,Tactical,Violent,Co-op,Realistic,Story Rich,Atmospheric,Mature,Online Co-Op,Gore,Third-Person Shooter,Third Person |
| Unturned | 2,017 | free | 75,000,000 | 555,368 | 91.2% | 3 | Action,Adventure,Casual,Indie,Free To Play | Free to Play,Survival,Zombies,Multiplayer,Open World,Co-op,Sandbox,Crafting,Shooter,Adventure,Post-apocalyptic,First-Person,Singleplayer,Looter Shooter,FPS,Action,Massively Multiplayer,Indie,Atmospheric,Casual |

### Top 10 Games by total_reviews
| Name | release_year | price_bucket | owners_mid | total_reviews | positive_rate | platform_count | Genres | Tags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Counter-Strike 2 | 2,012 | free | 150,000,000 | 8,815,087 | 86.7% | 2 | Action,Free To Play | FPS,Shooter,Multiplayer,Competitive,Action,Team-Based,e-sports,Tactical,First-Person,PvP,Online Co-Op,Co-op,Strategy,Military,War,Difficult,Trading,Realistic,Fast-Paced,Moddable |
| PUBG: BATTLEGROUNDS | 2,017 | free | 150,000,000 | 2,557,944 | 59.4% | 1 | Action,Adventure,Massively Multiplayer,Free To Play | Survival,Shooter,Battle Royale,Multiplayer,FPS,PvP,Third-Person Shooter,Action,Online Co-Op,Tactical,Co-op,First-Person,Strategy,Early Access,Competitive,Third Person,Team-Based,Difficult,Simulation,Stealth |
| Dota 2 | 2,013 | free | 150,000,000 | 2,498,969 | 81.5% | 3 | Action,Strategy,Free To Play | Free to Play,MOBA,Multiplayer,Strategy,e-sports,Team-Based,Competitive,Action,Online Co-Op,PvP,Difficult,Co-op,RTS,RPG,Tower Defense,Fantasy,Character Customization,Replay Value,Action RPG,Simulation |
| Grand Theft Auto V Legacy | 2,015 | free | 75,000,000 | 1,990,556 | 87.4% | 1 | Action,Adventure | Open World,Action,Multiplayer,Crime,Automobile Sim,Third Person,First-Person,Mature,Shooter,Adventure,Singleplayer,Third-Person Shooter,Racing,Co-op,Sandbox,Atmospheric,Funny,Great Soundtrack,Comedy,Moddable |
| Terraria | 2,011 | budget | 35,000,000 | 1,409,473 | 97.5% | 3 | Action,Adventure,Indie,RPG | Open World Survival Craft,Sandbox,Survival,2D,Multiplayer,Adventure,Pixel Graphics,Crafting,Building,Exploration,Co-op,Open World,Online Co-Op,Indie,Action,RPG,Singleplayer,Replay Value,Platformer,Atmospheric |
| Tom Clancy's Rainbow Six® Siege X | 2,015 | free | 35,000,000 | 1,398,584 | 83.9% | 1 | Action,Free To Play | FPS,PvP,Multiplayer,Tactical,e-sports,Shooter,Competitive,Online Co-Op,Action,Hero Shooter,Team-Based,Military,Strategy,First-Person,Co-op,Realistic,War,Destruction,Difficult,3D |
| Rust | 2,018 | mid | 35,000,000 | 1,227,784 | 87.2% | 2 | Action,Adventure,Indie,Massively Multiplayer,RPG | Survival,Crafting,Multiplayer,Open World,Open World Survival Craft,Building,PvP,Sandbox,Adventure,First-Person,Action,Nudity,FPS,Shooter,Co-op,Online Co-Op,Indie,Post-apocalyptic,Early Access,Simulation |
| Team Fortress 2 | 2,007 | free | 75,000,000 | 1,161,472 | 89.9% | 2 | Action,Free To Play | Free to Play,Hero Shooter,Multiplayer,FPS,Shooter,Action,Class-Based,Team-Based,Funny,First-Person,Online Co-Op,Competitive,Cartoony,Trading,Co-op,Comedy,Robots,Tactical,Cartoon,Crafting |
| Garry's Mod | 2,006 | budget | 35,000,000 | 1,159,707 | 96.8% | 3 | Casual,Indie,Simulation | Sandbox,Moddable,Multiplayer,Physics,Building,Casual,Funny,First-Person,Singleplayer,FPS,Simulation,Comedy,Online Co-Op,Co-op,Shooter,Action,Indie,PvP,Realistic,Exploration |
| Black Myth: Wukong | 2,024 | premium | 75,000,000 | 1,150,098 | 96.7% | 1 | Action,Adventure,RPG | Mythology,Action RPG,Action,Souls-like,RPG,Combat,Story Rich,Singleplayer,Action-Adventure,Drama,Dark Fantasy,Atmospheric,Adventure,3D,Fantasy,Hack and Slash,Difficult,Third Person,Music,Violent |

### Top 10 Rated Games by positive_rate (minimum 20 reviews)
| Name | release_year | price_bucket | owners_mid | total_reviews | positive_rate | platform_count | Genres | Tags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 秘封旅行 ~ Secret Sealing Travel | 2,020 | budget | 10,000 | 242 | 100.0% | 1 | Casual,Indie,RPG,Simulation,Early Access | Indie,Early Access,Casual,RPG,Simulation,Faith,Anime |
| Shooters, Ready! | 2,025 | budget | 35,000 | 229 | 100.0% | 1 | Action,Casual,Indie,Sports | FPS,Cute,Arcade,Shooter,Score Attack,Sports,Story Rich,Female Protagonist,Modern,Singleplayer,Action,Rogue-lite,First-Person,Tactical,3D,Combat,Casual,Indie,Sniper |
| Meddl Dash | 2,024 | budget | 10,000 | 228 | 100.0% | 1 | Action,Adventure,Racing,Simulation,Sports | Adventure,Action,Racing,Simulation,Sports,Action-Adventure,Action RPG,Dating Sim,Automobile Sim,God Game,3D Platformer,Outbreak Sim,Exploration,Immersive Sim,Combat Racing,Political Sim,3D,Third Person,Atmospheric,Dark Humor |
| Once Upon a Jester | 2,022 | budget | 10,000 | 208 | 100.0% | 1 | Action,Adventure,Casual,Indie | Story Rich,Adventure,Cute,Casual,Indie,2D,Mystery,Funny,Cartoon,Exploration,Music,Rhythm,Interactive Fiction,Choices Matter,Action-Adventure,Colorful,Singleplayer,Comedy,Side Scroller,Drama |
| Bakahazard 1+2 | 2,024 | budget | 10,000 | 198 | 100.0% | 1 | Adventure,RPG | Adventure,Memes,Comedy,Drama,Turn-Based Combat,Pixel Graphics,Zombies,Fantasy,Modern,Story Rich,Linear,Singleplayer,2D,RPG,Top-Down,RPGMaker,Anime,JRPG,CRPG |
| The Silent Kingdom | 2,025 | mid | 10,000 | 194 | 100.0% | 1 | Adventure,Indie,RPG,Early Access | JRPG,Otome,Story Rich,Turn-Based Combat,Choices Matter,Female Protagonist,Romance,Anime,Adventure,Dark Fantasy,Exploration,Multiple Endings,Visual Novel,2D,Emotional,RPG,Singleplayer,Sexual Content,Drama,Early Access |
| MareQuest: An Interactive Tail | 2,023 | budget | 75,000 | 190 | 100.0% | 1 | Adventure,Casual,Indie,RPG | Visual Novel,RPG,Cute,Adventure,Procedural Generation,Hand-drawn,Interactive Fiction,Choices Matter,Strategy RPG,Choose Your Own Adventure,2D,Colorful,Funny,Emotional,Fantasy,Horses,Relaxing,Character Customization,Multiple Endings,Resource Management |
| UOS Prototype | 2,020 | free | 10,000 | 185 | 100.0% | 1 | Early Access | Early Access,3D,VR |
| Misericorde Volume Two: White Wool & Snow | 2,024 | budget | 35,000 | 175 | 100.0% | 1 | Indie | Adventure,Visual Novel,Historical,Mystery,Medieval,Female Protagonist,Story Rich,Hand-drawn,2D,Text-Based,Stylized,Drama,Horror,Noir,Psychological Horror,Romance,Linear,Singleplayer,Indie,LGBTQ+ |
| PRODUCER 2021 | 2,022 | budget | 75,000 | 167 | 100.0% | 1 | Adventure,RPG,Simulation | Adventure,RPG,Interactive Fiction,Point & Click,Visual Novel,CRPG,Exploration,Immersive Sim,Choose Your Own Adventure,2D,Abstract,Colorful,Stylized,Psychedelic,1980s,Alternate History,Atmospheric,Automation,Aliens,Cyberpunk |

### Potential Hidden Gems (Heuristic Candidates)
Heuristic only (not model predictions): positive_rate >= 85%, total_reviews >= 20, and owners_mid at or below candidate median.

| Name | release_year | price_bucket | owners_mid | total_reviews | positive_rate | platform_count | Genres | Tags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 秘封旅行 ~ Secret Sealing Travel | 2,020 | budget | 10,000 | 242 | 100.0% | 1 | Casual,Indie,RPG,Simulation,Early Access | Indie,Early Access,Casual,RPG,Simulation,Faith,Anime |
| Meddl Dash | 2,024 | budget | 10,000 | 228 | 100.0% | 1 | Action,Adventure,Racing,Simulation,Sports | Adventure,Action,Racing,Simulation,Sports,Action-Adventure,Action RPG,Dating Sim,Automobile Sim,God Game,3D Platformer,Outbreak Sim,Exploration,Immersive Sim,Combat Racing,Political Sim,3D,Third Person,Atmospheric,Dark Humor |
| Once Upon a Jester | 2,022 | budget | 10,000 | 208 | 100.0% | 1 | Action,Adventure,Casual,Indie | Story Rich,Adventure,Cute,Casual,Indie,2D,Mystery,Funny,Cartoon,Exploration,Music,Rhythm,Interactive Fiction,Choices Matter,Action-Adventure,Colorful,Singleplayer,Comedy,Side Scroller,Drama |
| Bakahazard 1+2 | 2,024 | budget | 10,000 | 198 | 100.0% | 1 | Adventure,RPG | Adventure,Memes,Comedy,Drama,Turn-Based Combat,Pixel Graphics,Zombies,Fantasy,Modern,Story Rich,Linear,Singleplayer,2D,RPG,Top-Down,RPGMaker,Anime,JRPG,CRPG |
| The Silent Kingdom | 2,025 | mid | 10,000 | 194 | 100.0% | 1 | Adventure,Indie,RPG,Early Access | JRPG,Otome,Story Rich,Turn-Based Combat,Choices Matter,Female Protagonist,Romance,Anime,Adventure,Dark Fantasy,Exploration,Multiple Endings,Visual Novel,2D,Emotional,RPG,Singleplayer,Sexual Content,Drama,Early Access |
| UOS Prototype | 2,020 | free | 10,000 | 185 | 100.0% | 1 | Early Access | Early Access,3D,VR |
| Little Adventurer Treasure Hunt | 2,025 | budget | 10,000 | 152 | 100.0% | 1 | Adventure,Casual,Indie | Point & Click,Hidden Object,Casual,Puzzle,Hand-drawn,Cute,Tabletop,Exploration,Adventure,Word Game,Top-Down,Cartoon,Creature Collector,2D Platformer,Puzzle-Platformer,Stylized,Drama,Comedy,Family Friendly,2D |
| TETRACHROMA | 2,024 | budget | 10,000 | 151 | 100.0% | 1 | Action,Casual | Puzzle,Arcade,Casual,Action,Indie,Score Attack,Colorful,Controller,Pixel Graphics,2D,Retro,Singleplayer,1990's,1980s |
| Stuffo the Puzzle Bot | 2,023 | budget | 10,000 | 143 | 100.0% | 1 | Adventure,Indie | Puzzle-Platformer,Puzzle,Logic,2D,Relaxing,Pixel Graphics,Controller,Minimalist,Sci-fi,Robots,Adventure,Old School,Retro,Singleplayer,Soundtrack,Indie |
| 真夜的居所 - Chanye's Home | 2,023 | budget | 10,000 | 141 | 100.0% | 2 | Casual,Indie,RPG | Indie,RPG,LGBTQ+,Female Protagonist,Interactive Fiction,Anime,Story Rich,Cute,First-Person,Pixel Graphics,Word Game,Visual Novel,Relaxing,Casual,Comic Book,Cartoon,Singleplayer,2D |

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
