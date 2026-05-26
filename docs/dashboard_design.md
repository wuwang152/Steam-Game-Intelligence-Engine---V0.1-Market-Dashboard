# Dashboard Design Notes (V0.3 Planning)

## V0.3 visual upgrade direction

V0.3 focuses on improving dashboard communication quality through:

- clearer information hierarchy per page,
- richer visual patterns (cards, quadrants, rankings, heatmap-like summaries),
- tighter coupling between backend aggregation tables and UI widgets,
- presentation assets that explain **system logic** rather than duplicating dynamic chart output.

## Page-specific visualization suggestions

### Home
- KPI cards for high-level counts and health metrics.
- System flow diagram for the three-layer architecture.
- Short project overview and usage boundaries.

### 市场结构
- Line or area chart for release trend over time.
- Bar chart and/or treemap-style views for price bucket and owner-tier distributions.
- Platform count distribution as a compact structural view.

### 口碑与热度
- Ranking tables for review volume and top-rated games.
- Reputation-attention quadrant for sentiment vs. engagement positioning.
- Review-bucket positive-rate analysis for quality tiers.

### 赛道与本地化
- Genre, tag, and category distribution tables.
- Localization heatmap-style presentation for language support depth.
- Genre-localization cross view for market-fit scanning.

### 机会识别
- Opportunity cards for key candidate cohorts.
- Quadrant chart for risk/opportunity segmentation.
- Heuristic ranking tables with concise strategy notes.

## Figure usage policy (docs/assets)

Use figures under `docs/assets/` when they improve understanding of architecture or analysis logic. Avoid static images that simply duplicate dynamic Streamlit charts that are already rendered from live tables.


## 前端组件化（PR 2）

- 新增 `app/components/` 统一承载轻量 UI 复用组件：`cards.py`、`charts.py`、`figure_panel.py`、`source_badge.py`。
- `Home.py` 与 `4_机会识别.py` 优先使用组件进行 KPI、说明卡片、来源标识与可选图展示，保持后端表缺失时的兜底行为。
