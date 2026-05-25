import streamlit as st
import pandas as pd

from app.dashboard_table_loader import load_dashboard_table
from app.utils import PRICE_BUCKET_LABELS, get_available_columns, map_display_series, rename_display_columns, require_processed_data

PRICE_BUCKET_ORDER = ["free", "budget", "mid", "premium", "luxury"]
GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
PRICE_BUCKET_CN = {"free": "免费", "budget": "低价", "mid": "中价", "premium": "高价", "luxury": "豪华价位"}


def _show_missing_table_warning(*table_names: str) -> None:
    st.warning("未检测到对应的后端聚合表。请先运行 generate_dashboard_tables.py 生成后端分析表。")
    st.caption(f"缺失表：{', '.join([f'{name}.csv' for name in table_names])}")
    st.code(GEN_CMD, language="bash")


def _pct(v):
    return f"{v:.1%}" if v == v else "—"

st.title("价格与变现")
df = require_processed_data()

st.subheader("价格分层结构")
price_bucket_df = load_dashboard_table("price_bucket_distribution")
if price_bucket_df is not None and not price_bucket_df.empty and {"price_bucket", "count", "share", "median_positive_rate_reviewed"}.issubset(price_bucket_df.columns):
    st.caption("全量样本后端聚合结果")
    st.caption("价格分层结构优先读取后端聚合表 price_bucket_distribution.csv，确保数量、占比与口碑中位数口径一致。")
    display_df = price_bucket_df.copy()
    display_df["price_bucket_cn"] = display_df["price_bucket"].map(lambda x: PRICE_BUCKET_CN.get(str(x), str(x)))
    display_df["price_bucket"] = pd.Categorical(display_df["price_bucket"], categories=PRICE_BUCKET_ORDER, ordered=True)
    display_df = display_df.sort_values("price_bucket")
    chart_df = display_df.set_index("price_bucket_cn")["count"]
    st.bar_chart(chart_df)
    preview = display_df[["price_bucket_cn", "count", "share", "median_positive_rate_reviewed"]].copy()
    preview["count"] = preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    preview["share"] = preview["share"].map(_pct)
    preview["median_positive_rate_reviewed"] = preview["median_positive_rate_reviewed"].map(_pct)
    st.dataframe(preview, use_container_width=True)
else:
    _show_missing_table_warning("price_bucket_distribution")
    st.caption("当前筛选样本结果")
    if "price_bucket" in df.columns:
        bucket_series = map_display_series(df["price_bucket"], PRICE_BUCKET_LABELS)
        ordered = [x for x in PRICE_BUCKET_ORDER if x in bucket_series.unique()]
        remainder = sorted([x for x in bucket_series.unique() if x not in ordered])
        st.bar_chart(bucket_series.value_counts().reindex(ordered + remainder, fill_value=0))

if "Price" in df.columns:
    st.subheader("免费与付费占比")
    free_paid = df["Price"].fillna(0).apply(lambda x: "免费" if x == 0 else "付费").value_counts()
    st.bar_chart(free_paid)

owners_df = load_dashboard_table("owners_tier_distribution")
st.subheader("估计拥有者分层")
if owners_df is not None and not owners_df.empty and {"owners_tier", "count", "share", "median_total_reviews", "median_positive_rate_reviewed"}.issubset(owners_df.columns):
    st.caption("全量样本后端聚合结果")
    st.caption("估计拥有者分层基于 owners_mid 的后端聚合结果，仅代表区间中点估计，不等同于精确销量。")
    owners_chart = owners_df.set_index("owners_tier")["count"]
    st.bar_chart(owners_chart)
    owners_preview = owners_df[["owners_tier", "count", "share", "median_total_reviews", "median_positive_rate_reviewed"]].copy()
    owners_preview["count"] = owners_preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    owners_preview["share"] = owners_preview["share"].map(_pct)
    owners_preview["median_total_reviews"] = owners_preview["median_total_reviews"].map(lambda x: f"{int(x):,}" if x == x else "—")
    owners_preview["median_positive_rate_reviewed"] = owners_preview["median_positive_rate_reviewed"].map(_pct)
    st.dataframe(owners_preview, use_container_width=True)
elif "price_bucket" in df.columns and "total_reviews" in df.columns:
    _show_missing_table_warning("owners_tier_distribution")
    st.caption("当前筛选样本结果")
    st.subheader("各价格分层评论数中位数")
    median_reviews = df.groupby("price_bucket", dropna=True)["total_reviews"].median()
    order = [x for x in PRICE_BUCKET_ORDER if x in median_reviews.index]
    remainder = [x for x in median_reviews.index if x not in order]
    median_reviews = median_reviews.reindex(order + sorted(remainder))
    display_reviews = median_reviews.copy()
    display_reviews.index = [PRICE_BUCKET_LABELS.get(str(x), str(x)) for x in display_reviews.index]
    st.bar_chart(display_reviews)

platform_df = load_dashboard_table("platform_count_distribution")
st.subheader("平台支持数量分布")
if platform_df is not None and not platform_df.empty and {"platform_count", "count", "share"}.issubset(platform_df.columns):
    st.caption("全量样本后端聚合结果")
    st.caption("platform_count 表示 Windows / Mac / Linux 三个平台中被支持的平台数量。")
    st.bar_chart(platform_df.sort_values("platform_count").set_index("platform_count")["count"])
    p_preview = platform_df[["platform_count", "count", "share"]].copy().sort_values("platform_count")
    p_preview["count"] = p_preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    p_preview["share"] = p_preview["share"].map(_pct)
    st.dataframe(p_preview, use_container_width=True)
else:
    _show_missing_table_warning("platform_count_distribution")

st.subheader("价格与变现表")
table_cols = get_available_columns(df, ["Name", "Price", "Discount", "DLC count", "price_bucket"])
if table_cols:
    display_df = df[table_cols].head(250).copy()
    if "price_bucket" in display_df.columns:
        display_df["price_bucket"] = map_display_series(display_df["price_bucket"], PRICE_BUCKET_LABELS)
    st.dataframe(rename_display_columns(display_df), use_container_width=True)
else:
    st.info("缺少可展示的价格或变现相关列。")
