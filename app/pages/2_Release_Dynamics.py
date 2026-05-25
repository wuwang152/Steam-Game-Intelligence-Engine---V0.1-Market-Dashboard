import streamlit as st

from app.utils import require_processed_data

st.title("发行趋势")
df = require_processed_data()

if "release_year" not in df.columns or not df["release_year"].notna().any():
    st.warning("数据集中不包含 release_year，无法展示发行趋势图。")
    st.stop()

release_counts = df.groupby("release_year", dropna=True).size().rename("款游戏").sort_index()
st.subheader("各年份发行游戏数")
st.caption("展示处理后数据集中每年的游戏发行数量。")
st.caption("最近年份和未来年份的数据可能不完整。")
st.line_chart(release_counts)

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
        st.caption("好评率对有评论的游戏更有参考意义。")
        st.line_chart(yearly_ratio)
