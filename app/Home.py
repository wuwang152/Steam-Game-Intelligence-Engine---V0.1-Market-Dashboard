"""Steam Game Intelligence Engine dashboard home page."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from app.components import insight_card, method_note, metric_row, show_optional_figure, source_badge
from app.dashboard_table_loader import load_summary_metrics_row
from app.utils import load_processed_data

st.set_page_config(page_title="Steam 游戏市场智能分析与机会识别看板", layout="wide")

SUMMARY_METRICS_GENERATE_CMD = (
    "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv "
    "--output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _show_kpis(df: pd.DataFrame) -> None:
    st.subheader("核心指标")
    summary_metrics = load_summary_metrics_row()

    if summary_metrics is not None:
        source_badge("后端聚合表")
        st.caption("后端聚合表反映全量样本口径；若页面存在筛选器，请注意筛选结果与全量指标的区别。")

        def _fmt_int(metric_name: str) -> str:
            value = pd.to_numeric(summary_metrics.get(metric_name), errors="coerce")
            if pd.isna(value):
                return "N/A"
            return f"{int(round(float(value))):,}"

        def _fmt_pct(metric_name: str) -> str:
            value = pd.to_numeric(summary_metrics.get(metric_name), errors="coerce")
            if pd.isna(value):
                return "N/A"
            return f"{float(value):.1%}"

        metric_row(
            [
                {"label": "游戏总数", "value": _fmt_int("total_games")},
                {"label": "有评论游戏数", "value": _fmt_int("games_with_reviews")},
                {"label": "有评论占比", "value": _fmt_pct("share_with_reviews")},
                {"label": "估计拥有者中位数", "value": _fmt_int("median_owners_mid")},
                {"label": "评论数中位数", "value": _fmt_int("median_total_reviews")},
                {"label": "好评率中位数", "value": _fmt_pct("median_positive_rate_reviewed")},
                {"label": "简中支持占比", "value": _fmt_pct("simplified_chinese_support_share")},
                {"label": "免费游戏占比", "value": _fmt_pct("free_share")},
            ],
            columns=4,
        )
        return

    st.warning("未检测到 summary_metrics.csv，以下展示为处理后数据的兜底统计。")
    st.code(SUMMARY_METRICS_GENERATE_CMD, language="bash")

    metric_row(
        [
            {"label": "游戏总数", "value": f"{len(df):,}"},
            {
                "label": "发行年份覆盖",
                "value": f"{int(df['release_year'].min())}–{int(df['release_year'].max())}" if "release_year" in df.columns and df["release_year"].notna().any() else "N/A",
            },
            {"label": "价格中位数", "value": f"${pd.to_numeric(df['Price'], errors='coerce').median():.2f}" if "Price" in df.columns else "N/A"},
            {"label": "评论数中位数", "value": f"{pd.to_numeric(df['total_reviews'], errors='coerce').median():,.0f}" if "total_reviews" in df.columns else "N/A"},
        ],
        columns=4,
    )


def main() -> None:
    st.title("Steam 游戏市场智能分析与机会识别看板")

    st.subheader("项目总览")
    source_badge("文档说明 + 后端聚合表")
    st.caption("面向 Steam 市场结构、口碑热度、赛道本地化与机会识别的中文分析看板。")
    insight_card("看板目标", "将原始数据处理结果转化为可读的市场结构画像与启发式机会线索，支持快速定位重点赛道。")

    df = load_processed_data()
    if df is None:
        st.warning(
            "未在 data/processed/steam_games_cleaned.csv 找到处理后数据。"
            "请先运行数据流水线后再访问看板。"
        )
        st.stop()

    _show_kpis(df)

    st.subheader("数据管道说明")
    st.markdown(
        "- 数据清洗：`scripts/run_pipeline.py` 生成标准化数据集。\n"
        "- 后端聚合：`scripts/generate_dashboard_tables.py` 生成看板表。\n"
        "- 前端展示：页面优先读取聚合表，缺失时使用兜底逻辑保证可用。"
    )
    method_note("该看板以可解释的统计与规则聚合为核心，不直接输出机器学习预测结论。")

    st.subheader("页面导航")
    c1, c2 = st.columns(2)
    with c1:
        insight_card("1_市场结构", "年度发行、价格分层、拥有者分层与平台覆盖。")
        insight_card("2_口碑与热度", "评论热度、口碑分布及风险观察。")
        insight_card("3_赛道与本地化", "类型/标签/分类结构与语言支持特征。")
    with c2:
        insight_card("4_机会识别", "热门、口碑、隐藏潜力与本地化机会候选榜单。")
        insight_card("5_后端聚合表预览", "用于诊断后端表生成状态与单表内容。")

    st.subheader("系统流程图")
    shown = show_optional_figure(REPOSITORY_ROOT / "docs" / "assets" / "system_flow.png", caption="系统流程图（可选）")
    if not shown:
        st.caption("未检测到 docs/assets/system_flow.png，已跳过流程图展示。")


main()
