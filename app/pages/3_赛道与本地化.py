import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import LANGUAGE_LABELS, format_ranking_table_for_display, require_processed_data, top_split_values_cached

GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"


def _warn_missing(*tables: str) -> None:
    st.warning("未检测到对应后端聚合表，已切换到页面兜底逻辑。")
    st.caption(f"缺失表：{', '.join([f'{t}.csv' for t in tables])}")
    st.code(GEN_CMD, language="bash")


st.title("赛道与本地化")
df = require_processed_data()

top_n = st.slider("Top N", min_value=5, max_value=50, value=20, step=5)

for title, table_name, key_col in [
    ("热门游戏类型", "genre_distribution", "genre"),
    ("热门标签", "tag_distribution", "tag"),
    ("功能分类", "category_distribution", "category"),
]:
    st.subheader(title)
    t = load_dashboard_table(table_name)
    if t is not None and {key_col, "count"}.issubset(t.columns):
        st.bar_chart(t.set_index(key_col)["count"].head(top_n))
        st.dataframe(format_ranking_table_for_display(t.head(top_n)), use_container_width=True)
    else:
        _warn_missing(table_name)

st.subheader("语言支持概况")
lang = load_dashboard_table("language_support_summary")
if lang is not None and {"language", "count", "share"}.issubset(lang.columns):
    l = lang.copy()
    l["language"] = l["language"].map(lambda x: LANGUAGE_LABELS.get(str(x), str(x)))
    st.dataframe(format_ranking_table_for_display(l), use_container_width=True)
else:
    _warn_missing("language_support_summary")

st.subheader("各类型本地化覆盖")
loc = load_dashboard_table("localization_by_genre")
if loc is not None and not loc.empty:
    st.dataframe(format_ranking_table_for_display(loc.head(top_n)), use_container_width=True)
else:
    _warn_missing("localization_by_genre")
    if "Genres" in df.columns:
        st.bar_chart(top_split_values_cached(df["Genres"], sep=";", top_n=top_n))
