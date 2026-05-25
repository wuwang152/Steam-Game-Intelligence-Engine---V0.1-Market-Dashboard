import streamlit as st

from app.dashboard_table_loader import (
    EXPECTED_DASHBOARD_TABLES,
    dashboard_tables_status,
    list_available_dashboard_tables,
    list_missing_dashboard_tables,
    load_required_dashboard_table,
)

st.title("后端分析表预览")
st.write("本页用于检查后端聚合表和榜单表是否已生成。生成表来自 data/processed/dashboard_tables/，不会自动提交到 GitHub。")

available_tables = list_available_dashboard_tables()
missing_tables = list_missing_dashboard_tables()
status_df = dashboard_tables_status()

c1, c2, c3 = st.columns(3)
c1.metric("预期表数量", len(EXPECTED_DASHBOARD_TABLES))
c2.metric("已生成表数量", len(available_tables))
c3.metric("缺失表数量", len(missing_tables))

status_display_df = status_df.rename(
    columns={
        "table_name": "表名",
        "filename": "文件名",
        "exists": "是否存在",
        "rows": "行数",
        "columns": "列数",
        "size_bytes": "文件大小（字节）",
    }
)
st.subheader("表状态")
st.dataframe(status_display_df, use_container_width=True)

if missing_tables:
    st.warning(
        "检测到缺失表。请先运行以下命令生成后端分析表：\n\n"
        "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv "
        "--output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"
    )

st.subheader("单表预览")
if not available_tables:
    st.info("当前没有可预览的后端分析表。")
else:
    selected_table = st.selectbox("选择要预览的表", options=available_tables)
    preview_df = load_required_dashboard_table(selected_table)

    st.write(f"已选择表：`{selected_table}`")
    st.write(f"行数：{len(preview_df)}")
    st.write(f"列数：{preview_df.shape[1]}")
    st.dataframe(preview_df.head(100), use_container_width=True)
