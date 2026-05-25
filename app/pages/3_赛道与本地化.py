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

st.subheader("热门游戏类型")
genre_table = load_dashboard_table("genre_distribution")
if genre_table is not None and {"genre", "count"}.issubset(genre_table.columns):
    st.bar_chart(genre_table.set_index("genre")["count"].head(top_n))
    st.dataframe(format_ranking_table_for_display(genre_table.head(top_n)), use_container_width=True)
else:
    _warn_missing("genre_distribution")
    if "Genres" in df.columns:
        st.caption("当前处理后数据兜底结果")
        st.bar_chart(top_split_values_cached(df["Genres"], sep=";", top_n=top_n))

st.subheader("热门标签")
tag_table = load_dashboard_table("tag_distribution")
if tag_table is not None and {"tag", "count"}.issubset(tag_table.columns):
    st.bar_chart(tag_table.set_index("tag")["count"].head(top_n))
    st.dataframe(format_ranking_table_for_display(tag_table.head(top_n)), use_container_width=True)
else:
    _warn_missing("tag_distribution")
    if "Tags" in df.columns:
        st.caption("当前处理后数据兜底结果")
        st.bar_chart(top_split_values_cached(df["Tags"], sep=";", top_n=top_n))

st.subheader("功能分类")
category_table = load_dashboard_table("category_distribution")
if category_table is not None and {"category", "count"}.issubset(category_table.columns):
    st.bar_chart(category_table.set_index("category")["count"].head(top_n))
    st.dataframe(format_ranking_table_for_display(category_table.head(top_n)), use_container_width=True)
else:
    _warn_missing("category_distribution")
    if "Categories" in df.columns:
        st.caption("当前处理后数据兜底结果")
        st.bar_chart(top_split_values_cached(df["Categories"], sep=";", top_n=top_n))

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
        st.caption("当前处理后数据兜底结果")
        st.bar_chart(top_split_values_cached(df["Genres"], sep=";", top_n=top_n))
