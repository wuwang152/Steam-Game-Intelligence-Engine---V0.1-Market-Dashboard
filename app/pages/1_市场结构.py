import pandas as pd
import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import PRICE_BUCKET_LABELS, format_ranking_table_for_display, map_display_series, require_processed_data

GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"


def _warn_missing(*tables: str) -> None:
    st.warning("未检测到对应后端聚合表，已切换到页面兜底逻辑。")
    st.caption(f"缺失表：{', '.join([f'{t}.csv' for t in tables])}")
    st.code(GEN_CMD, language="bash")


st.title("市场结构")
df = require_processed_data()

st.subheader("年度发行结构")
yearly = load_dashboard_table("yearly_release_counts")
if yearly is not None and {"release_year", "count"}.issubset(yearly.columns):
    chart = yearly[["release_year", "count"]].sort_values("release_year").set_index("release_year")
    st.bar_chart(chart["count"])
    st.dataframe(format_ranking_table_for_display(yearly[[c for c in ["release_year", "count", "share"] if c in yearly.columns]]), use_container_width=True)
else:
    _warn_missing("yearly_release_counts")
    if "release_year" in df.columns:
        fallback = pd.to_numeric(df["release_year"], errors="coerce").dropna().astype(int).value_counts().sort_index()
        st.bar_chart(fallback)

st.subheader("价格分层结构")
price = load_dashboard_table("price_bucket_distribution")
if price is not None and {"price_bucket", "count"}.issubset(price.columns):
    p = price.copy()
    p["price_bucket"] = map_display_series(p["price_bucket"], PRICE_BUCKET_LABELS)
    st.bar_chart(p.set_index("price_bucket")["count"])
    st.dataframe(format_ranking_table_for_display(p[[c for c in ["price_bucket", "count", "share", "median_positive_rate_reviewed"] if c in p.columns]]), use_container_width=True)
else:
    _warn_missing("price_bucket_distribution")
    if "price_bucket" in df.columns:
        st.bar_chart(map_display_series(df["price_bucket"], PRICE_BUCKET_LABELS).value_counts())

st.subheader("估计拥有者分层")
owners = load_dashboard_table("owners_tier_distribution")
if owners is not None and {"owners_tier", "count"}.issubset(owners.columns):
    st.bar_chart(owners.set_index("owners_tier")["count"])
    st.dataframe(format_ranking_table_for_display(owners[[c for c in ["owners_tier", "count", "share", "median_total_reviews", "median_positive_rate_reviewed"] if c in owners.columns]]), use_container_width=True)
else:
    _warn_missing("owners_tier_distribution")
st.caption("owners_mid 为 Steam 拥有者区间的中点估计，不代表精确销量。")

st.subheader("平台覆盖结构")
platform = load_dashboard_table("platform_count_distribution")
if platform is not None and {"platform_count", "count"}.issubset(platform.columns):
    p = platform.sort_values("platform_count")
    st.bar_chart(p.set_index("platform_count")["count"])
    st.dataframe(format_ranking_table_for_display(p[[c for c in ["platform_count", "count", "share"] if c in p.columns]]), use_container_width=True)
else:
    _warn_missing("platform_count_distribution")
st.caption("platform_count 表示 Windows / Mac / Linux 三个平台中被支持的平台数量。")
st.caption("后端聚合表反映全量样本口径；若页面存在筛选器，请注意筛选结果与全量指标的区别。")
