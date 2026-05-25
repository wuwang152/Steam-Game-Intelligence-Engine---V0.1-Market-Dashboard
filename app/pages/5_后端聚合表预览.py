import streamlit as st

from app.dashboard_table_loader import (
    EXPECTED_DASHBOARD_TABLES,
    dashboard_tables_status,
    list_available_dashboard_tables,
    list_missing_dashboard_tables,
    load_required_dashboard_table,
)

GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"

st.title("后端聚合表预览")
st.caption("后端聚合表反映全量样本口径；若页面存在筛选器，请注意筛选结果与全量指标的区别。")

available = list_available_dashboard_tables()
missing = list_missing_dashboard_tables()
status = dashboard_tables_status()

c1, c2, c3 = st.columns(3)
c1.metric("预期表数量", len(EXPECTED_DASHBOARD_TABLES))
c2.metric("可用表数量", len(available))
c3.metric("缺失表数量", len(missing))

st.subheader("状态总览")
st.dataframe(
    status.rename(columns={
        "table_name": "表名",
        "filename": "文件名",
        "exists": "是否存在",
        "rows": "行数",
        "columns": "列数",
        "size_bytes": "文件大小（字节）",
    }),
    use_container_width=True,
)

if missing:
    st.warning("检测到缺失后端聚合表，请先执行生成命令。")
    st.code(GEN_CMD, language="bash")

st.subheader("单表预览")
if available:
    selected = st.selectbox("选择表名", options=available)
    preview = load_required_dashboard_table(selected)
    st.caption(f"当前表：{selected} | 行数：{len(preview)} | 列数：{preview.shape[1]}")
    st.dataframe(preview.head(100), use_container_width=True)
else:
    st.info("暂无可预览的后端聚合表。")
