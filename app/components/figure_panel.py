"""Optional figure rendering helpers."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def show_optional_figure(path: str | Path, caption: str | None = None) -> bool:
    figure_path = Path(path)
    if not figure_path.is_file():
        return False

    st.image(str(figure_path), use_container_width=True)
    if caption:
        st.caption(caption)
    return True
