# Steam Game Intelligence Engine

## 项目定位

Steam Game Intelligence Engine 是一个面向 Steam 游戏市场的可复现分析项目，用于把原始游戏数据清洗、标准化并转化为可解释的市场结构、口碑热度、赛道本地化和机会识别线索。项目以描述性分析和启发式规则为主，适合用于数据处理演示、市场观察、看板展示和后续建模前的分析基线建设。

当前稳定发布版本：V0.2

当前开发阶段：V0.3（开发中，尚未正式发布）

## 当前 V0.2 稳定能力

- **数据清洗流水线：** 标准化字段类型、平台标记和行级数据质量检查。
- **分析特征工程：** 构建发行时间、拥有者区间估计、评论比例、评论信号、价格分层和元数据密度等特征。
- **数据校验：** 使用脚本检查输出 schema、关键字段完整性和基础数据质量约束。
- **自动化测试：** 使用 pytest 覆盖特征工程和边界情况。
- **市场洞察报告：** 可从处理后数据生成 Markdown 报告，便于复盘和展示。
- **Streamlit 看板：** 提供当前多页面中文看板，用于查看市场结构、口碑热度、赛道本地化、机会识别和后端聚合表。

## 当前 V0.3 开发方向

V0.3 仍处于开发中，重点不是发布新的预测模型，而是提升看板的信息表达和数据来源透明度：

- 梳理数据源、处理层和展示层之间的数据血缘关系。
- 将首页和页面说明调整为更清晰的中文展示体验。
- 使用后端聚合表支持更稳定的前端展示。
- 增加可被 Git 文本 diff 追踪的说明型 SVG 资产。
- 保持原始数据和本地生成数据不进入仓库提交。

## 仓库结构

- `.github/workflows/` — CI workflow definitions。
- `app/` — Streamlit dashboard entrypoint and page modules。
- `data/raw/` — 全量原始数据集的本地放置目录。
- `data/processed/` — 本地生成的清洗和特征工程输出目录。
- `data/sample/` — 用于演示、测试和校验的示例数据集。
- `docs/` — 项目文档和说明资产。
- `notebooks/` — exploratory analysis notebooks。
- `reports/` — 生成的报告和分析产物。
- `scripts/` — 数据流水线、校验和报告生成脚本。
- `src/steam_intelligence/` — core package logic。
- `tests/` — automated unit tests。

## 数据集放置策略

仓库内包含可复现的示例数据集：

- `data/sample/games_sample.csv`

全量原始数据应仅保存在本地目录：

- `data/raw/`

约定的全量原始数据路径为：

- `data/raw/steam_games.csv`

以下内容不应提交到 GitHub：

- `data/raw/` 中的原始数据。
- `data/processed/` 中的本地生成数据。
- `data/processed/dashboard_tables/` 中的本地生成聚合表。

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

### PowerShell equivalents (Windows)

```powershell
# Set PYTHONPATH for current PowerShell session
$env:PYTHONPATH = "src"

# Run tests
python -m pytest -q

# Run validation
python .\scripts\validate_data.py --input .\data\processed\steam_games_cleaned.csv

# Generate the V0.2 market report
python .\scripts\generate_market_report.py --input .\data\processed\steam_games_cleaned.csv --output .\reports\steam_market_insights_v0.2.md

# Launch Streamlit
streamlit run .\app\Home.py
```

## 当前看板页面结构

当前 Streamlit 看板页面如下：

- `app/Home.py`
- `app/pages/1_市场结构.py`
- `app/pages/2_口碑与热度.py`
- `app/pages/3_赛道与本地化.py`
- `app/pages/4_机会识别.py`
- `app/pages/5_后端聚合表预览.py`

这些页面覆盖市场结构、口碑与热度、赛道与本地化、机会识别，以及后端聚合表预览。

## 首页 SVG 系统流程图

首页新增中文三层架构流程图，用于向仓库访问者和看板用户说明数据源层、处理与聚合层、Streamlit 中文展示层之间的数据血缘关系。

流程图文件路径为：

- `docs/assets/system_flow.svg`

该文件是纯文本 SVG 资产，可被 Git 文本 diff 追踪，不需要提交 PNG、JPG、PDF 或其他二进制图像。可通过以下命令重新生成：

```bash
python scripts/generate_system_flow_svg.py
```

## 后端聚合表生成

V0.3 开发阶段的看板页面优先读取本地生成的后端聚合表。可使用以下命令生成：

```bash
python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20
```

## 市场洞察报告

V0.2 提供可复现的 Markdown 市场洞察报告生成流程：

- 报告产物：[`reports/steam_market_insights_v0.2.md`](reports/steam_market_insights_v0.2.md)
- 输入文件：`data/processed/steam_games_cleaned.csv`
- 生成脚本：`scripts/generate_market_report.py`
- 方法边界：当前报告只包含描述性指标，不包含因果推断或机器学习预测。

生成报告命令：

```bash
PYTHONPATH=src python scripts/generate_market_report.py --input data/processed/steam_games_cleaned.csv --output reports/steam_market_insights_v0.2.md
```

## Dashboard screenshots

### Home dashboard

![Home dashboard](docs/assets/dashboard_home.png)

### Attention distribution

![Attention distribution](docs/assets/dashboard_attention.png)

### Genre and tag explorer

![Genre and tag explorer](docs/assets/dashboard_genre_tag.png)

## 测试与 CI

### Local testing

本地校验建议运行：

```bash
PYTHONPATH=src python scripts/validate_data.py --input data/processed/steam_games_cleaned.csv
PYTHONPATH=src pytest -q
```

### Continuous Integration

GitHub Actions 会在 push 和 pull request 时运行仓库检查，包括依赖安装、自动化测试和校验步骤。

## 局限性

- `owners_mid` 是拥有者区间的估计中点，不代表精确销量。
- `positive_rate` 对有评论的游戏更有解释意义。
- 隐藏精品、低价高口碑和本地化机会等结果来自启发式规则，不是机器学习预测。
- 当前分析是描述性分析，不是因果分析。
- 全量数据需要由使用者在本地放置，仓库不提交原始数据或本地生成数据。

## Roadmap

- **V0.3 direction:** improve source transparency and dashboard presentation assets.
- **V0.3 direction:** refine backend aggregation tables and reusable UI components.
- **Future direction:** game segmentation.
- **Future direction:** ranking score system.
- **Future direction:** genre/tag opportunity analysis.
- **Future direction:** predictive modeling after descriptive analytics baselines are stable.

## V0.2 development status

- V0.2 Step 1 交付分析特征基础。
- V0.2 Step 2 增加 Streamlit 市场洞察能力，用于筛选 KPI 和市场结构分析。
- V0.2 Step 3 改善筛选器、KPI、图表和榜单区域的可读性。
- V0.2 Step 4 增加可复现的 Markdown Market Insights 报告生成流程。
- V0.2 Step 5 提升看板一致性与可读性。
- V0.2 Step 6 重新生成全量处理数据的 Market Insights 报告产物。
- V0.2 Step 7 聚焦 README 和项目展示清理。
