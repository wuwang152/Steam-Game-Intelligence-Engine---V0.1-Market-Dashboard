import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import (
    get_available_columns,
    rename_display_columns,
    require_processed_data,
    top_split_values_cached,
)
GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
LANG_CN = {"simplified_chinese": "简体中文", "english": "英文", "japanese": "日文", "korean": "韩文", "chinese_audio": "中文语音"}


def _show_missing_table_warning(*table_names: str) -> None:
    st.warning("未检测到对应的后端聚合表。请先运行 generate_dashboard_tables.py 生成后端分析表。")
    st.caption(f"缺失表：{', '.join([f'{name}.csv' for name in table_names])}")
    st.code(GEN_CMD, language="bash")


def _pct(v):
    return f"{v:.1%}" if v == v else "—"

st.title("类型/标签探索")
df = require_processed_data()

st.sidebar.header("类型/标签筛选")
top_n = st.sidebar.slider("Top N 数量", min_value=5, max_value=50, value=20, step=5)

if "tag_count" in df.columns and df["tag_count"].notna().any():
    max_tag_count = int(df["tag_count"].max())
    min_tags = st.sidebar.slider("最小标签数（tag_count）", min_value=0, max_value=max_tag_count, value=0)
    filtered_df = df[df["tag_count"].fillna(0) >= min_tags].copy()
else:
    filtered_df = df.copy()

st.subheader("热门游戏类型")
genre_dist = load_dashboard_table("genre_distribution")
if genre_dist is not None and not genre_dist.empty and {"genre", "count", "share", "median_positive_rate_reviewed", "simplified_chinese_support_share"}.issubset(genre_dist.columns):
    st.caption("全量样本后端聚合结果")
    st.bar_chart(genre_dist.set_index("genre")["count"].head(top_n))
    g_preview = genre_dist[["genre", "count", "share", "median_positive_rate_reviewed", "simplified_chinese_support_share"]].head(top_n).copy()
    g_preview["count"] = g_preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    g_preview["share"] = g_preview["share"].map(_pct)
    g_preview["median_positive_rate_reviewed"] = g_preview["median_positive_rate_reviewed"].map(_pct)
    g_preview["simplified_chinese_support_share"] = g_preview["simplified_chinese_support_share"].map(_pct)
    st.dataframe(g_preview, use_container_width=True)
elif "Genres" in filtered_df.columns:
    _show_missing_table_warning("genre_distribution")
    st.caption("当前筛选样本结果")
    genre_counts = top_split_values_cached(filtered_df["Genres"], sep=";", top_n=top_n)
else:
    genre_counts = None
if genre_counts is not None and not genre_counts.empty:
    st.bar_chart(genre_counts)
else:
    st.info("Genres 列缺失或为空。")

st.subheader("热门标签")
tag_dist = load_dashboard_table("tag_distribution")
if tag_dist is not None and not tag_dist.empty and {"tag", "count", "share", "median_positive_rate_reviewed", "simplified_chinese_support_share"}.issubset(tag_dist.columns):
    st.caption("全量样本后端聚合结果")
    st.bar_chart(tag_dist.set_index("tag")["count"].head(top_n))
    t_preview = tag_dist[["tag", "count", "share", "median_positive_rate_reviewed", "simplified_chinese_support_share"]].head(top_n).copy()
    t_preview["count"] = t_preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    t_preview["share"] = t_preview["share"].map(_pct)
    t_preview["median_positive_rate_reviewed"] = t_preview["median_positive_rate_reviewed"].map(_pct)
    t_preview["simplified_chinese_support_share"] = t_preview["simplified_chinese_support_share"].map(_pct)
    st.dataframe(t_preview, use_container_width=True)
elif "Tags" in filtered_df.columns:
    _show_missing_table_warning("tag_distribution")
    st.caption("当前筛选样本结果")
    tag_counts = top_split_values_cached(filtered_df["Tags"], sep=";", top_n=top_n)
else:
    tag_counts = None
if tag_counts is not None and not tag_counts.empty:
    st.bar_chart(tag_counts)
else:
    st.info("Tags 列缺失或为空。")

st.subheader("热门分类")
cat_dist = load_dashboard_table("category_distribution")
if cat_dist is not None and not cat_dist.empty and {"category", "count", "share", "median_positive_rate_reviewed"}.issubset(cat_dist.columns):
    st.caption("全量样本后端聚合结果")
    st.bar_chart(cat_dist.set_index("category")["count"].head(top_n))
    c_preview = cat_dist[["category", "count", "share", "median_positive_rate_reviewed"]].head(top_n).copy()
    c_preview["count"] = c_preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    c_preview["share"] = c_preview["share"].map(_pct)
    c_preview["median_positive_rate_reviewed"] = c_preview["median_positive_rate_reviewed"].map(_pct)
    st.dataframe(c_preview, use_container_width=True)
else:
    _show_missing_table_warning("category_distribution")

st.subheader("语言支持概览")
lang_dist = load_dashboard_table("language_support_summary")
if lang_dist is not None and not lang_dist.empty and {"language", "count", "share"}.issubset(lang_dist.columns):
    st.caption("全量样本后端聚合结果")
    l_preview = lang_dist[["language", "count", "share"]].copy()
    l_preview["language"] = l_preview["language"].map(lambda x: LANG_CN.get(str(x), str(x)))
    l_preview["count"] = l_preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    l_preview["share"] = l_preview["share"].map(_pct)
    st.dataframe(l_preview, use_container_width=True)
else:
    _show_missing_table_warning("language_support_summary")

st.subheader("按类型观察本地化支持")
loc_genre = load_dashboard_table("localization_by_genre")
if loc_genre is not None and not loc_genre.empty:
    st.caption("全量样本后端聚合结果")
    st.caption("本地化结构基于后端聚合表 localization_by_genre.csv，可用于观察不同类型下的语言支持差异。")
    loc_preview = loc_genre.head(top_n).copy()
    for col in ["simplified_chinese_support_share", "english_support_share", "japanese_support_share", "korean_support_share", "median_positive_rate_reviewed"]:
        if col in loc_preview.columns:
            loc_preview[col] = loc_preview[col].map(_pct)
    if "count" in loc_preview.columns:
        loc_preview["count"] = loc_preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    st.dataframe(loc_preview, use_container_width=True)
else:
    _show_missing_table_warning("localization_by_genre")

st.subheader("筛选游戏表")
table_cols = get_available_columns(filtered_df, ["Name", "Genres", "Tags", "genre_count", "tag_count", "positive_ratio"])
if table_cols:
    st.dataframe(rename_display_columns(filtered_df[table_cols].head(300)), use_container_width=True)
else:
    st.info("缺少可用于类型/标签展示的标准列。")
