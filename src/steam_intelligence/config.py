"""Project-level constants and defaults."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "steam_games.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "steam_games_cleaned.csv"

OWNER_RANGE_COL = "Estimated owners"
RELEASE_DATE_COL = "Release date"
