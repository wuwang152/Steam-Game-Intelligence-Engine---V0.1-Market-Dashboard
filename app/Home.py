"""Steam Game Intelligence Engine dashboard home page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.dashboard_table_loader import load_summary_metrics_row
from app.utils import load_processed_data

st.set_page_config(page_title="Steam 游戏市场智能分析与机会识别看板", layout="wide")

SUMMARY_METRICS_GENERATE_CMD = (
    "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv "
    "--output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
)


def _show_kpis(df: pd.DataFrame) -> None:
    st.subheader("核心指标")
    summary_metrics = load_summary_metrics_row()

    if summary_metrics is not None:
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

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("游戏总数", _fmt_int("total_games"))
        m2.metric("有评论游戏数", _fmt_int("games_with_reviews"))
        m3.metric("有评论占比", _fmt_pct("share_with_reviews"))
        m4.metric("估计拥有者中位数", _fmt_int("median_owners_mid"))

        m5, m6, m7, m8 = st.columns(4)
        m5.metric("评论数中位数", _fmt_int("median_total_reviews"))
        m6.metric("好评率中位数", _fmt_pct("median_positive_rate_reviewed"))
        m7.metric("简中支持占比", _fmt_pct("simplified_chinese_support_share"))
        m8.metric("免费游戏占比", _fmt_pct("free_share"))
        return

    st.warning("未检测到 summary_metrics.csv，以下展示为处理后数据的兜底统计。")
    st.code(SUMMARY_METRICS_GENERATE_CMD, language="bash")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("游戏总数", f"{len(df):,}")
    k2.metric("发行年份覆盖", f"{int(df['release_year'].min())}–{int(df['release_year'].max())}" if "release_year" in df.columns and df["release_year"].notna().any() else "N/A")
    k3.metric("价格中位数", f"${pd.to_numeric(df['Price'], errors='coerce').median():.2f}" if "Price" in df.columns else "N/A")
    k4.metric("评论数中位数", f"{pd.to_numeric(df['total_reviews'], errors='coerce').median():,.0f}" if "total_reviews" in df.columns else "N/A")


def main() -> None:
    st.title("Steam 游戏市场智能分析与机会识别看板")

    st.subheader("项目总览")
    st.caption("面向 Steam 市场结构、口碑热度、赛道本地化与机会识别的中文分析看板。")

    df = load_processed_data()
    if df is None:
        st.warning(
            "未在 data/processed/steam_games_cleaned.csv 找到处理后数据。"
            "请先运行数据流水线后再访问看板。"
        )
        st.stop()

    _show_kpis(df)

    st.subheader("数据管道说明")
    st.caption("前端页面优先读取后端聚合表；缺失时自动使用轻量兜底逻辑，保证页面可用。")

    st.subheader("页面导航说明")
    st.markdown(
        "- **市场结构**：年度发行、价格分层、拥有者分层与平台覆盖。\n"
        "- **口碑与热度**：评论热度、口碑分布及风险观察。\n"
        "- **赛道与本地化**：类型/标签/分类与语言支持结构。\n"
        "- **机会识别**：热门、口碑、机会与本地化候选榜单。\n"
        "- **后端聚合表预览**：诊断后端表生成状态与单表内容。"
    )


main()
