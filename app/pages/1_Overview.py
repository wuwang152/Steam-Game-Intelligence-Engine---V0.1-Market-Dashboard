import streamlit as st
import pandas as pd

from app.dashboard_table_loader import load_summary_metrics_row
from app.utils import PRICE_BUCKET_LABELS, get_available_columns, map_display_series, rename_display_columns, require_processed_data

PRICE_BUCKET_ORDER = ["free", "budget", "mid", "premium", "luxury"]
SUMMARY_METRICS_GENERATE_CMD = (
    "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv "
    "--output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
)

st.title("总览")
df = require_processed_data()
filtered_df = df.copy()

st.sidebar.header("总览筛选")
if "release_year" in filtered_df.columns and filtered_df["release_year"].notna().any():
    year_min = int(filtered_df["release_year"].min())
    year_max = int(filtered_df["release_year"].max())
    year_range = st.sidebar.slider("发行年份", min_value=year_min, max_value=year_max, value=(year_min, year_max))
    filtered_df = filtered_df[filtered_df["release_year"].between(year_range[0], year_range[1], inclusive="both")]

if "price_bucket" in filtered_df.columns:
    options = [b for b in PRICE_BUCKET_ORDER if b in filtered_df["price_bucket"].dropna().astype(str).unique()]
    option_labels = {x: PRICE_BUCKET_LABELS.get(x, x) for x in options}
    selected_labels = st.sidebar.multiselect(
        "价格分层",
        options=[option_labels[x] for x in options],
        default=[option_labels[x] for x in options],
    )
    selected_buckets = [k for k, v in option_labels.items() if v in selected_labels]
    if selected_buckets:
        filtered_df = filtered_df[filtered_df["price_bucket"].astype(str).isin(selected_buckets)]

summary_metrics = load_summary_metrics_row()
if summary_metrics is not None:
    st.markdown("#### 全量样本核心指标")
    st.caption(
        "以下核心指标来自后端聚合表 summary_metrics.csv，反映全量样本口径，不随左侧筛选器变化；"
        "下方图表和数据预览仍会随筛选条件更新。"
    )

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

    st.markdown("##### 核心规模")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("游戏总数", _fmt_int("total_games"))
    m2.metric("有评论游戏数", _fmt_int("games_with_reviews"))
    m3.metric("有评论占比", _fmt_pct("share_with_reviews"))
    m4.metric("估计拥有者中位数", _fmt_int("median_owners_mid"))

    st.markdown("##### 口碑与价格")
    m5, m6, m7, m8 = st.columns(4)
    m5.metric("评论数中位数", _fmt_int("median_total_reviews"))
    m6.metric("好评率中位数", _fmt_pct("median_positive_rate_reviewed"))
    m7.metric("免费游戏占比", _fmt_pct("free_share"))
    m8.metric("折扣游戏占比", _fmt_pct("discount_share"))

    st.markdown("##### 语言与元数据覆盖")
    m9, m10, m11, m12 = st.columns(4)
    m9.metric("简中支持占比", _fmt_pct("simplified_chinese_support_share"))
    m10.metric("英文支持占比", _fmt_pct("english_support_share"))
    m11.metric("有标签数据游戏数", _fmt_int("games_with_tags"))
    m12.metric("有开发商数据游戏数", _fmt_int("games_with_developer"))
else:
    st.warning("未检测到后端总览指标表。请先运行 generate_dashboard_tables.py 生成后端分析表。")
    st.code(SUMMARY_METRICS_GENERATE_CMD, language="bash")

    m1, m2, m3 = st.columns(3)
    m1.metric("筛选后游戏数", f"{len(filtered_df):,}")
    if "Price" in filtered_df.columns:
        m2.metric("价格中位数", f"${filtered_df['Price'].median():.2f}")
    else:
        m2.metric("价格中位数", "N/A")
    if "positive_ratio" in filtered_df.columns:
        m3.metric("好评率中位数", f"{filtered_df['positive_ratio'].median():.1%}")
    else:
        m3.metric("好评率中位数", "N/A")

preview_cols = get_available_columns(
    filtered_df,
    ["Name", "release_year", "Price", "price_bucket", "owners_mid", "total_reviews", "positive_ratio"],
)
st.subheader("筛选数据预览")
if preview_cols:
    display_df = filtered_df[preview_cols].head(300).copy()
    if "owners_mid" in display_df.columns:
        display_df["owners_mid"] = display_df["owners_mid"].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
    if "total_reviews" in display_df.columns:
        display_df["total_reviews"] = display_df["total_reviews"].map(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
    if "positive_ratio" in display_df.columns:
        display_df["positive_ratio"] = display_df["positive_ratio"].map(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
    if "price_bucket" in display_df.columns:
        display_df["price_bucket"] = map_display_series(display_df["price_bucket"], PRICE_BUCKET_LABELS)
    st.dataframe(rename_display_columns(display_df), use_container_width=True)
else:
    st.info("数据集中缺少可用于总览的标准列。")
