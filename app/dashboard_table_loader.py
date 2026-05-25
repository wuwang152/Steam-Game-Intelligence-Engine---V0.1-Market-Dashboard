from pathlib import Path

import pandas as pd

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_TABLE_DIR = REPOSITORY_ROOT / "data" / "processed" / "dashboard_tables"

EXPECTED_DASHBOARD_TABLES = [
    "summary_metrics",
    "yearly_release_counts",
    "price_bucket_distribution",
    "owners_tier_distribution",
    "platform_count_distribution",
    "review_signal_distribution",
    "review_sentiment_distribution",
    "review_bucket_positive_rate",
    "genre_distribution",
    "tag_distribution",
    "category_distribution",
    "language_support_summary",
    "localization_by_genre",
    "top_games_by_owners",
    "top_games_by_reviews",
    "top_rated_games",
    "hidden_gems",
    "low_price_high_rating",
    "high_attention_low_rating",
    "chinese_supported_potential",
    "localization_opportunities",
]


def _resolve_base_dir(base_dir: Path | None = None) -> Path:
    return base_dir if base_dir is not None else DASHBOARD_TABLE_DIR


def get_dashboard_table_path(table_name: str, base_dir: Path | None = None) -> Path:
    return _resolve_base_dir(base_dir) / f"{table_name}.csv"


def dashboard_table_exists(table_name: str, base_dir: Path | None = None) -> bool:
    return get_dashboard_table_path(table_name, base_dir=base_dir).is_file()


def list_available_dashboard_tables(base_dir: Path | None = None) -> list[str]:
    return [name for name in EXPECTED_DASHBOARD_TABLES if dashboard_table_exists(name, base_dir=base_dir)]


def list_missing_dashboard_tables(base_dir: Path | None = None) -> list[str]:
    return [name for name in EXPECTED_DASHBOARD_TABLES if not dashboard_table_exists(name, base_dir=base_dir)]


def load_dashboard_table(table_name: str, base_dir: Path | None = None) -> pd.DataFrame | None:
    path = get_dashboard_table_path(table_name, base_dir=base_dir)
    if not path.is_file():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


def load_required_dashboard_table(table_name: str, base_dir: Path | None = None) -> pd.DataFrame:
    df = load_dashboard_table(table_name, base_dir=base_dir)
    if df is None:
        return pd.DataFrame()
    return df


def load_summary_metrics_row(base_dir: Path | None = None) -> pd.Series | None:
    df = load_dashboard_table("summary_metrics", base_dir=base_dir)
    if df is None or df.empty:
        return None
    return df.iloc[0]


def dashboard_tables_status(base_dir: Path | None = None) -> pd.DataFrame:
    rows: list[dict] = []
    for table_name in EXPECTED_DASHBOARD_TABLES:
        path = get_dashboard_table_path(table_name, base_dir=base_dir)
        exists = path.is_file()
        size_bytes = path.stat().st_size if exists else 0

        n_rows = 0
        n_cols = 0
        if exists:
            try:
                table_df = pd.read_csv(path)
                n_rows, n_cols = table_df.shape
            except Exception:
                n_rows = -1
                n_cols = -1

        rows.append(
            {
                "table_name": table_name,
                "filename": path.name,
                "exists": exists,
                "rows": n_rows,
                "columns": n_cols,
                "size_bytes": size_bytes,
            }
        )

    return pd.DataFrame(rows)
