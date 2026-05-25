import streamlit as st

from app.utils import (
    get_available_columns,
    rename_display_columns,
    require_processed_data,
    top_split_values_cached,
)

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
if "Genres" in filtered_df.columns:
    genre_counts = top_split_values_cached(filtered_df["Genres"], sep=";", top_n=top_n)
else:
    genre_counts = None
if genre_counts is not None and not genre_counts.empty:
    st.bar_chart(genre_counts)
else:
    st.info("Genres 列缺失或为空。")

st.subheader("热门标签")
if "Tags" in filtered_df.columns:
    tag_counts = top_split_values_cached(filtered_df["Tags"], sep=";", top_n=top_n)
else:
    tag_counts = None
if tag_counts is not None and not tag_counts.empty:
    st.bar_chart(tag_counts)
else:
    st.info("Tags 列缺失或为空。")

st.subheader("筛选游戏表")
table_cols = get_available_columns(filtered_df, ["Name", "Genres", "Tags", "genre_count", "tag_count", "positive_ratio"])
if table_cols:
    st.dataframe(rename_display_columns(filtered_df[table_cols].head(300)), use_container_width=True)
else:
    st.info("缺少可用于类型/标签展示的标准列。")
