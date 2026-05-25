import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import require_processed_data

GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"


def _show_missing_table_warning(table_name: str) -> None:
    st.warning("未检测到对应的后端聚合表。请先运行 generate_dashboard_tables.py 生成后端聚合表。")
    st.caption(f"缺失表：{table_name}.csv")
    st.code(GEN_CMD, language="bash")


def _fmt_pct(series):
    return series.map(lambda x: f"{x:.1%}" if x == x else "—")


st.title("发行趋势")
df = require_processed_data()

if "release_year" not in df.columns or not df["release_year"].notna().any():
    st.warning("数据集中不包含 release_year，无法展示发行趋势图。")
    st.stop()

st.subheader("各年份发行游戏数")
yearly_df = load_dashboard_table("yearly_release_counts")
if yearly_df is not None and not yearly_df.empty and {"release_year", "count", "share"}.issubset(yearly_df.columns):
    st.caption("全量样本后端聚合结果")
    st.caption("年度发行数量优先读取后端聚合表 yearly_release_counts.csv，反映全量样本的年度供给结构。")
    chart_df = yearly_df[["release_year", "count"]].copy().sort_values("release_year")
    chart_df = chart_df.set_index("release_year")
    st.bar_chart(chart_df["count"])
    preview = yearly_df[["release_year", "count", "share"]].copy().sort_values("release_year")
    preview["count"] = preview["count"].map(lambda x: f"{int(x):,}" if x == x else "—")
    preview["share"] = _fmt_pct(preview["share"])
    st.dataframe(preview.head(20), use_container_width=True)
else:
    _show_missing_table_warning("yearly_release_counts")
    st.caption("当前筛选样本结果")
    release_counts = df.groupby("release_year", dropna=True).size().rename("款游戏").sort_index()
    st.caption("展示处理后数据集中每年的游戏发行数量。")
    st.caption("最近年份和未来年份的数据可能不完整。")
    st.bar_chart(release_counts)

if "Price" in df.columns:
    yearly_price = df.groupby("release_year", dropna=True)["Price"].median().dropna().sort_index()
    if not yearly_price.empty:
        st.subheader("各年份价格中位数")
        st.caption("该曲线展示首发定价的长期变化。")
        st.line_chart(yearly_price)

if "positive_ratio" in df.columns:
    yearly_ratio = df.groupby("release_year", dropna=True)["positive_ratio"].median().dropna().sort_index()
    if not yearly_ratio.empty:
        st.subheader("各年份好评率中位数")
        st.caption("该曲线反映不同发行年份的玩家口碑中位变化。")
        st.caption("好评率仅在有评论样本中更具解释意义。")
        st.line_chart(yearly_ratio)
