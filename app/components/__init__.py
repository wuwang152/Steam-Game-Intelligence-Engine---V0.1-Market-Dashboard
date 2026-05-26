"""Reusable dashboard UI components."""

from app.components.cards import insight_card, method_note, metric_row, warning_note
from app.components.charts import show_bar_distribution, show_line_trend, show_scatter_quadrant, show_table_preview
from app.components.figure_panel import show_optional_figure
from app.components.source_badge import source_badge

__all__ = [
    "metric_row",
    "insight_card",
    "method_note",
    "warning_note",
    "show_bar_distribution",
    "show_line_trend",
    "show_scatter_quadrant",
    "show_table_preview",
    "show_optional_figure",
    "source_badge",
]
