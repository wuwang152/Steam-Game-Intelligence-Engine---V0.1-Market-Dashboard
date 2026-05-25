import importlib.util
from pathlib import Path

import pandas as pd

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_data.py"
spec = importlib.util.spec_from_file_location("validate_data", MODULE_PATH)
validate_data = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validate_data)
run_checks = validate_data.run_checks


def _base_row():
    return {
        "AppID": 1,
        "Name": "Demo",
        "Price": 0.0,
        "release_year": 2020,
        "owners_low": 0,
        "owners_high": 0,
        "owners_mid": 0,
        "total_reviews": 0,
        "positive_rate": 0.0,
        "review_log": 0.0,
        "has_reviews": False,
        "is_free": True,
        "has_discount": False,
        "platform_count": 1,
        "price_bucket": "free",
        "has_valid_metascore": False,
        "has_valid_user_score": False,
        "has_peak_ccu": False,
        "has_recommendations": False,
        "has_playtime_forever": False,
        "has_recent_playtime": False,
        "has_genres": False,
        "has_tags": False,
        "has_categories": False,
        "has_developer": False,
        "has_publisher": False,
        "has_header_image": False,
        "has_screenshots": False,
        "has_about_text": False,
        "supports_simplified_chinese": False,
        "supports_english": False,
        "supports_japanese": False,
        "supports_korean": False,
        "has_chinese_audio": False,
        "supported_language_count": 0,
        "full_audio_language_count": 0,
    }


def test_validation_accepts_bool_like_strings_and_non_negative_counts():
    row = _base_row()
    row["has_reviews"] = "False"
    row["supports_english"] = "true"
    row["supported_language_count"] = "2"
    row["full_audio_language_count"] = 0
    df = pd.DataFrame([row])
    assert run_checks(df) == []


def test_validation_rejects_invalid_bool_like_and_negative_counts():
    row = _base_row()
    row["has_valid_metascore"] = "maybe"
    row["supported_language_count"] = -1
    df = pd.DataFrame([row])
    errors = run_checks(df)
    assert any("has_valid_metascore" in err for err in errors)
    assert any("supported_language_count" in err for err in errors)
