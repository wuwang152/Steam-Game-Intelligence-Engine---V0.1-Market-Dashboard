"""Reusable chart and table wrappers using Streamlit built-ins."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def _guard_df(df: pd.DataFrame | None, required_columns: list[str] | None = None) -> bool:
    if df is None or df.empty:
        st.info("暂无可展示数据。")
        return False
    required_columns = required_columns or []
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        st.info(f"缺少列：{', '.join(missing)}")
        return False
    return True


def show_bar_distribution(df: pd.DataFrame | None, x_col: str, y_col: str, title: str | None = None) -> None:
    if title:
        st.markdown(f"#### {title}")
    if not _guard_df(df, [x_col, y_col]):
        return
    chart_df = df[[x_col, y_col]].dropna().set_index(x_col)
    if chart_df.empty:
        st.info("暂无可展示数据。")
        return
    st.bar_chart(chart_df, y=y_col)


def show_line_trend(df: pd.DataFrame | None, x_col: str, y_col: str, title: str | None = None) -> None:
    if title:
        st.markdown(f"#### {title}")
    if not _guard_df(df, [x_col, y_col]):
        return
    chart_df = df[[x_col, y_col]].dropna().set_index(x_col)
    if chart_df.empty:
        st.info("暂无可展示数据。")
        return
    st.line_chart(chart_df, y=y_col)


def show_scatter_quadrant(df: pd.DataFrame | None, x_col: str, y_col: str, color_col: str | None = None, title: str | None = None) -> None:
    if title:
        st.markdown(f"#### {title}")
    cols = [x_col, y_col] + ([color_col] if color_col else [])
    if not _guard_df(df, [x_col, y_col]):
        return
    chart_df = df[cols].dropna(subset=[x_col, y_col])
    if chart_df.empty:
        st.info("暂无可展示数据。")
        return
    kwargs = {"x": x_col, "y": y_col}
    if color_col and color_col in chart_df.columns:
        kwargs["color"] = color_col
    st.scatter_chart(chart_df, **kwargs)


def show_table_preview(df: pd.DataFrame | None, title: str | None = None, max_rows: int = 20) -> None:
    if title:
        st.markdown(f"#### {title}")
    if df is None or df.empty:
        st.info("暂无可展示数据。")
        return
    st.dataframe(df.head(max_rows), use_container_width=True)
