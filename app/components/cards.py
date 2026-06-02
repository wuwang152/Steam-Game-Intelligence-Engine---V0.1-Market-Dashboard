"""Reusable card-style UI helpers for Streamlit pages."""

from __future__ import annotations

import streamlit as st


def metric_row(metrics: list[dict[str, str]], columns: int = 4) -> None:
    """Render a row-block of Streamlit metrics.

    Each metric dict accepts: label, value, and optional delta/help.
    """
    if not metrics:
        return

    chunk_size = max(1, int(columns))
    for start in range(0, len(metrics), chunk_size):
        chunk = metrics[start : start + chunk_size]
        cols = st.columns(len(chunk))
        for col, metric in zip(cols, chunk):
            with col:
                st.metric(
                    label=str(metric.get("label", "")),
                    value=str(metric.get("value", "N/A")),
                    delta=metric.get("delta"),
                    help=metric.get("help"),
                )


def insight_card(title: str, content: str) -> None:
    """Render a concise insight card."""
    st.markdown(f"##### {title}")
    st.info(content)


def method_note(content: str) -> None:
    """Render a method transparency note."""
    st.caption(f"方法说明：{content}")


def warning_note(content: str) -> None:
    """Render a warning note."""
    st.warning(content)
