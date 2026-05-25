import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.dashboard_table_loader import (
    EXPECTED_DASHBOARD_TABLES,
    dashboard_table_exists,
    dashboard_tables_status,
    get_dashboard_table_path,
    list_available_dashboard_tables,
    list_missing_dashboard_tables,
    load_dashboard_table,
    load_summary_metrics_row,
)


def test_expected_dashboard_tables_non_empty() -> None:
    assert EXPECTED_DASHBOARD_TABLES


def test_get_dashboard_table_path_has_csv_suffix(tmp_path) -> None:
    path = get_dashboard_table_path("summary_metrics", base_dir=tmp_path)
    assert path.suffix == ".csv"
    assert path.name == "summary_metrics.csv"


def test_dashboard_table_exists_false_for_missing(tmp_path) -> None:
    assert not dashboard_table_exists("summary_metrics", base_dir=tmp_path)


def test_load_dashboard_table_missing_returns_none(tmp_path) -> None:
    assert load_dashboard_table("summary_metrics", base_dir=tmp_path) is None


def test_load_summary_metrics_row_missing_returns_none(tmp_path) -> None:
    assert load_summary_metrics_row(base_dir=tmp_path) is None


def test_load_summary_metrics_row_empty_returns_none(tmp_path) -> None:
    pd.DataFrame(columns=["total_games"]).to_csv(tmp_path / "summary_metrics.csv", index=False)
    assert load_summary_metrics_row(base_dir=tmp_path) is None


def test_load_summary_metrics_row_returns_first_row(tmp_path) -> None:
    pd.DataFrame({"total_games": [100, 200], "share_with_reviews": [0.5, 0.7]}).to_csv(
        tmp_path / "summary_metrics.csv",
        index=False,
    )
    row = load_summary_metrics_row(base_dir=tmp_path)
    assert row is not None
    assert int(row["total_games"]) == 100


def test_dashboard_tables_status_with_no_files(tmp_path) -> None:
    status = dashboard_tables_status(base_dir=tmp_path)
    assert len(status) == len(EXPECTED_DASHBOARD_TABLES)
    assert (status["exists"] == False).all()  # noqa: E712
    assert (status["rows"] == 0).all()
    assert (status["columns"] == 0).all()
    assert (status["size_bytes"] == 0).all()


def test_dashboard_tables_status_reports_existing_csv(tmp_path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    csv_path = tmp_path / "summary_metrics.csv"
    df.to_csv(csv_path, index=False)

    status = dashboard_tables_status(base_dir=tmp_path)
    row = status.loc[status["table_name"] == "summary_metrics"].iloc[0]

    assert bool(row["exists"]) is True
    assert int(row["rows"]) == 2
    assert int(row["columns"]) == 2
    assert int(row["size_bytes"]) > 0


def test_available_and_missing_tables_lists(tmp_path) -> None:
    pd.DataFrame({"x": [1]}).to_csv(tmp_path / "summary_metrics.csv", index=False)
    pd.DataFrame({"x": [1]}).to_csv(tmp_path / "top_rated_games.csv", index=False)

    available = list_available_dashboard_tables(base_dir=tmp_path)
    missing = list_missing_dashboard_tables(base_dir=tmp_path)

    assert "summary_metrics" in available
    assert "top_rated_games" in available
    assert "summary_metrics" not in missing
    assert "top_rated_games" not in missing
    assert len(available) + len(missing) == len(EXPECTED_DASHBOARD_TABLES)
