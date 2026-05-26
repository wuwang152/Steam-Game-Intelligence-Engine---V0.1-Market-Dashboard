"""Simple source-semantic badge for dashboard sections."""

from __future__ import annotations

import streamlit as st


def source_badge(text: str) -> None:
    st.caption(f"来源：{text}")
