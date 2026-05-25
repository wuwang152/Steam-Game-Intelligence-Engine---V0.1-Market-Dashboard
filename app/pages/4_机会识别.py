import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import format_ranking_table_for_display

GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"


def _show(title: str, table: str) -> None:
    st.markdown(f"#### {title}")
    df = load_dashboard_table(table)
    if df is None or df.empty:
        st.warning(f"缺失后端表：{table}.csv")
        st.code(GEN_CMD, language="bash")
        return
    st.dataframe(format_ranking_table_for_display(df), use_container_width=True)


st.title("机会识别")
st.caption("机会识别榜单为透明启发式规则结果，不代表机器学习预测、因果结论或个性化推荐。")

st.subheader("热门榜单")
_show("估计拥有者热门游戏", "top_games_by_owners")
_show("评论数热门游戏", "top_games_by_reviews")

st.subheader("高口碑榜单")
_show("高口碑游戏", "top_rated_games")

st.subheader("机会识别")
_show("隐藏潜力游戏", "hidden_gems")
_show("低价高口碑", "low_price_high_rating")

st.subheader("本地化机会")
_show("已支持简中的潜力候选", "chinese_supported_potential")
_show("未支持简中的本地化机会", "localization_opportunities")

st.subheader("风险观察")
_show("高关注低口碑", "high_attention_low_rating")
