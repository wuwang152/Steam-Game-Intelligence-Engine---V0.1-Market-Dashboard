import pandas as pd
import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import (
    REVIEW_SENTIMENT_LABELS,
    format_percent,
    format_ranking_table_for_display,
    get_available_columns,
    map_display_series,
    rename_display_columns,
    require_processed_data,
)

REVIEW_SENTIMENT_ORDER = ["no_reviews", "weak", "mixed", "strong"]
GEN_CMD = (
    "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv "
    "--output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
)


def _backend_table_warning() -> None:
    st.warning("未检测到对应的后端聚合表。请先运行 generate_dashboard_tables.py 生成后端聚合表。")
    st.code(GEN_CMD)


st.title("口碑信号")
df = require_processed_data()

st.subheader("口碑情绪分布")
sentiment_df = load_dashboard_table("review_sentiment_distribution")
if sentiment_df is not None and not sentiment_df.empty and {"review_sentiment", "count"}.issubset(sentiment_df.columns):
    st.caption("全量样本后端聚合结果")
    chart_df = sentiment_df.copy()
    chart_df["review_sentiment_display"] = map_display_series(chart_df["review_sentiment"], REVIEW_SENTIMENT_LABELS)
    order_map = {k: i for i, k in enumerate(REVIEW_SENTIMENT_ORDER)}
    chart_df = chart_df.sort_values(by="review_sentiment", key=lambda s: s.map(lambda x: order_map.get(str(x), 999)))
    st.bar_chart(chart_df.set_index("review_sentiment_display")["count"])

    preview_cols = ["review_sentiment", "count", "share", "median_owners_mid", "median_total_reviews"]
    preview = sentiment_df[[c for c in preview_cols if c in sentiment_df.columns]].copy()
    st.dataframe(format_ranking_table_for_display(preview), use_container_width=True)
    st.caption("口碑情绪分布优先读取后端聚合表 review_sentiment_distribution.csv，反映全量样本的口碑结构。")
else:
    _backend_table_warning()
    st.caption("当前筛选样本结果")
    if "review_sentiment" in df.columns:
        sentiment_series = map_display_series(df["review_sentiment"], REVIEW_SENTIMENT_LABELS)
        order = [x for x in REVIEW_SENTIMENT_ORDER if x in sentiment_series.unique()]
        remainder = sorted([x for x in sentiment_series.unique() if x not in order])
        st.bar_chart(sentiment_series.value_counts().reindex(order + remainder, fill_value=0))

st.subheader("评论数分桶与好评率中位数")
bucket_df = load_dashboard_table("review_bucket_positive_rate")
if bucket_df is not None and not bucket_df.empty and {"review_bucket", "median_positive_rate_reviewed"}.issubset(bucket_df.columns):
    st.caption("全量样本后端聚合结果")
    chart_data = bucket_df[["review_bucket", "median_positive_rate_reviewed"]].dropna().set_index("review_bucket")
    st.bar_chart(chart_data)

    preview_cols = ["review_bucket", "count", "share", "median_positive_rate_reviewed", "median_owners_mid"]
    preview = bucket_df[[c for c in preview_cols if c in bucket_df.columns]].copy()
    st.dataframe(format_ranking_table_for_display(preview), use_container_width=True)
    st.caption("不同评论数量区间下的好评率中位数基于有评论游戏计算，可减少无评论样本对口碑判断的干扰。")
else:
    _backend_table_warning()
    st.caption("当前筛选样本结果")
    if "total_reviews" in df.columns and "positive_ratio" in df.columns:
        scatter_df = df[["total_reviews", "positive_ratio"]].dropna().copy()
        bins = [20, 100, 500, 1_000, 5_000, 10_000, 50_000, float("inf")]
        labels = ["20–100", "100–500", "500–1k", "1k–5k", "5k–10k", "10k–50k", "50k+"]
        scatter_df = scatter_df[scatter_df["total_reviews"] >= 20]
        scatter_df["评论数分桶"] = pd.cut(scatter_df["total_reviews"], bins=bins, labels=labels, right=False, include_lowest=True)
        bucket_median = (
            scatter_df.groupby("评论数分桶", observed=False)["positive_ratio"]
            .median()
            .mul(100)
            .rename("中位好评率（%）")
        )
        st.bar_chart(bucket_median.dropna(), x_label="评论数分桶", y_label="中位好评率（%）")

st.subheader("高口碑榜")
top_rated_df = load_dashboard_table("top_rated_games")
if top_rated_df is not None and not top_rated_df.empty:
    st.caption("全量样本后端聚合结果")
    display_cols = [
        "Name", "release_year", "price_bucket", "owners_mid", "total_reviews", "positive_rate", "supports_simplified_chinese", "Genres", "Tags"
    ]
    display_df = top_rated_df[[c for c in display_cols if c in top_rated_df.columns]].copy()
    st.dataframe(format_ranking_table_for_display(display_df), use_container_width=True)
    st.caption("高口碑榜要求达到最低评论数门槛，避免少量评论造成的极端好评率误导。")
else:
    _backend_table_warning()
    st.caption("当前筛选样本结果")
    if {"Name", "positive_ratio", "total_reviews"}.issubset(df.columns):
        filtered = df[df["total_reviews"].fillna(0) >= 20].copy()
        top_games = filtered.sort_values(["positive_ratio", "total_reviews"], ascending=[False, False]).head(30)
        top_games["positive_ratio"] = top_games["positive_ratio"].apply(format_percent)
        st.dataframe(rename_display_columns(top_games[["Name", "positive_ratio", "total_reviews"]]), use_container_width=True)
    else:
        preview_cols = get_available_columns(df, ["Name", "positive_ratio", "total_reviews"])
        if preview_cols:
            st.dataframe(rename_display_columns(df[preview_cols].head(30)), use_container_width=True)

st.subheader("高关注低口碑风险榜")
risk_df = load_dashboard_table("high_attention_low_rating")
if risk_df is not None and not risk_df.empty:
    st.caption("全量样本后端聚合结果")
    display_cols = [
        "Name", "release_year", "price_bucket", "owners_mid", "total_reviews", "positive_rate", "supports_simplified_chinese", "Genres", "Tags", "heuristic_reason"
    ]
    display_df = risk_df[[c for c in display_cols if c in risk_df.columns]].copy()
    st.dataframe(format_ranking_table_for_display(display_df), use_container_width=True)
    st.caption("该榜单为透明启发式筛选结果，用于识别评论量较高但好评率偏低的游戏，并非机器学习预测。")
else:
    _backend_table_warning()
