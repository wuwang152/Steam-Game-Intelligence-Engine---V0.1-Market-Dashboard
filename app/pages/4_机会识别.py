from pathlib import Path

import pandas as pd
import streamlit as st

from app.components import insight_card, method_note, metric_row, show_optional_figure, source_badge, warning_note
from app.dashboard_table_loader import load_dashboard_table
from app.utils import format_ranking_table_for_display

GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


TABLE_SECTIONS = [
    ("估计拥有者热门游戏", "top_games_by_owners", "热门榜单"),
    ("评论数热门游戏", "top_games_by_reviews", "热门榜单"),
    ("高口碑游戏", "top_rated_games", "高口碑榜单"),
    ("隐藏潜力游戏", "hidden_gems", "机会识别"),
    ("低价高口碑", "low_price_high_rating", "机会识别"),
    ("未支持简中的本地化机会", "localization_opportunities", "本地化机会"),
    ("高关注低口碑", "high_attention_low_rating", "风险观察"),
]


def _load_and_show_table(title: str, table: str) -> bool:
    st.markdown(f"#### {title}")
    df = load_dashboard_table(table)
    if df is None or df.empty:
        warning_note(f"缺失后端表：{table}.csv")
        st.code(GEN_CMD, language="bash")
        return False
    st.dataframe(format_ranking_table_for_display(df), use_container_width=True)
    return True


def _table_count(df: pd.DataFrame | None) -> str:
    if df is None or df.empty:
        return "0"
    return f"{len(df):,}"


st.title("机会识别")
source_badge("启发式机会识别结果")
st.caption("以下榜单用于市场研究与策略讨论，强调透明规则与可复核计算过程。")

st.subheader("机会总览")
st.markdown("围绕热度、口碑、价格与本地化四个维度，聚焦可执行的机会候选与风险信号。")

owners_df = load_dashboard_table("top_games_by_owners")
reviews_df = load_dashboard_table("top_games_by_reviews")
gems_df = load_dashboard_table("hidden_gems")
loc_df = load_dashboard_table("localization_opportunities")

metric_row(
    [
        {"label": "热门样本（拥有者）", "value": _table_count(owners_df)},
        {"label": "热门样本（评论）", "value": _table_count(reviews_df)},
        {"label": "隐藏潜力候选", "value": _table_count(gems_df)},
        {"label": "本地化机会候选", "value": _table_count(loc_df)},
    ],
    columns=4,
)

insight_card("解释边界", "机会识别结果来自显式启发式规则，不代表机器学习预测、因果结论或个性化推荐。")
method_note("请结合业务目标、发行阶段与品类上下文进行二次验证。")

st.subheader("机会识别逻辑图")
shown = show_optional_figure(REPOSITORY_ROOT / "docs" / "assets" / "opportunity_logic.png", caption="机会识别逻辑（可选）")
if not shown:
    st.caption("未检测到 docs/assets/opportunity_logic.png，已跳过逻辑图展示。")

current_section = None
for title, table, section in TABLE_SECTIONS:
    if section != current_section:
        st.subheader(section)
        current_section = section
    _load_and_show_table(title, table)
