import pandas as pd

from steam_intelligence.dashboard_tables import build_dashboard_tables, write_dashboard_tables


def sample_df():
    return pd.DataFrame([
        {"AppID": 1, "Name": "A", "release_year": 2023, "price_bucket": "free", "owners_mid": 5000, "total_reviews": 100, "positive_rate": 0.9, "supports_simplified_chinese": True, "supports_english": True, "supports_japanese": False, "supports_korean": False, "has_chinese_audio": False, "Genres": "Action;RPG", "Tags": "Indie,N/A", "Categories": "Single-player", "platform_count": 2, "review_signal": "low", "review_sentiment": "strong", "has_discount": False, "is_free": True},
        {"AppID": 2, "Name": "B", "release_year": 2021, "price_bucket": "budget", "owners_mid": 100000, "total_reviews": 1000, "positive_rate": 0.6, "supports_simplified_chinese": False, "supports_english": True, "supports_japanese": True, "supports_korean": True, "has_chinese_audio": False, "Genres": "None", "Tags": "N/A", "Categories": "nan", "platform_count": 1, "review_signal": "high", "review_sentiment": "mixed", "has_discount": True, "is_free": False},
        {"AppID": 3, "Name": "C", "release_year": 2020, "price_bucket": "premium", "owners_mid": 20000, "total_reviews": 50, "positive_rate": 0.95, "supports_simplified_chinese": False, "supports_english": True, "supports_japanese": False, "supports_korean": False, "has_chinese_audio": False, "Genres": "Strategy", "Tags": "Tactics", "Categories": "Multi-player", "platform_count": 3, "review_signal": "low", "review_sentiment": "strong", "has_discount": False, "is_free": False},
    ])


def test_build_tables_shapes_and_types():
    tables = build_dashboard_tables(sample_df(), top_n=30, min_reviews=20)
    required = {"summary_metrics","yearly_release_counts","price_bucket_distribution","owners_tier_distribution","platform_count_distribution","review_signal_distribution","review_sentiment_distribution","review_bucket_positive_rate","genre_distribution","tag_distribution","category_distribution","language_support_summary","localization_by_genre","top_games_by_owners","top_games_by_reviews","top_rated_games","hidden_gems","low_price_high_rating","high_attention_low_rating","chinese_supported_potential","localization_opportunities"}
    assert required.issubset(set(tables))
    assert all(isinstance(v, pd.DataFrame) for v in tables.values())


def test_distribution_has_count_share_and_valid_share_range():
    tables = build_dashboard_tables(sample_df())
    for name in ["yearly_release_counts", "platform_count_distribution", "review_bucket_positive_rate", "genre_distribution"]:
        assert {"count", "share"}.issubset(tables[name].columns)
        if not tables[name].empty:
            assert tables[name]["share"].dropna().between(0, 1).all()


def test_placeholders_excluded():
    tables = build_dashboard_tables(sample_df())
    assert "None" not in set(tables["genre_distribution"]["genre"].astype(str))
    assert "N/A" not in set(tables["tag_distribution"]["tag"].astype(str))
    assert "nan" not in set(tables["category_distribution"]["category"].astype(str))


def test_rankings_rules():
    tables = build_dashboard_tables(sample_df(), min_reviews=20)
    reviews = tables["top_games_by_reviews"]["total_reviews"].tolist()
    assert reviews == sorted(reviews, reverse=True)
    assert (tables["top_rated_games"]["total_reviews"] >= 20).all()
    assert (tables["hidden_gems"]["positive_rate"] >= 0.85).all()
    assert (tables["hidden_gems"]["total_reviews"] >= 20).all()
    if not tables["localization_opportunities"].empty:
        assert (~tables["localization_opportunities"]["supports_simplified_chinese"]).all()


def test_missing_optional_columns_do_not_crash():
    df = pd.DataFrame([{"AppID": 1, "Name": "A", "total_reviews": 0, "positive_rate": 0.0}])
    tables = build_dashboard_tables(df)
    assert isinstance(tables["genre_distribution"], pd.DataFrame)
    assert isinstance(tables["top_games_by_owners"], pd.DataFrame)


def test_write_dashboard_tables(tmp_path):
    tables = build_dashboard_tables(sample_df())
    out = tmp_path / "dash"
    write_dashboard_tables(tables, out)
    assert (out / "summary_metrics.csv").exists()
    assert (out / "top_games_by_reviews.csv").exists()
    assert not (tmp_path / "summary_metrics.csv").exists()


def test_top_n_share_uses_full_valid_denominator():
    df = pd.DataFrame([
        {"Name": "g1", "owners_mid": 1, "total_reviews": 1, "positive_rate": 1.0, "supports_simplified_chinese": False, "Tags": "A"},
        {"Name": "g2", "owners_mid": 1, "total_reviews": 1, "positive_rate": 1.0, "supports_simplified_chinese": False, "Tags": "A"},
        {"Name": "g3", "owners_mid": 1, "total_reviews": 1, "positive_rate": 1.0, "supports_simplified_chinese": False, "Tags": "A"},
        {"Name": "g4", "owners_mid": 1, "total_reviews": 1, "positive_rate": 1.0, "supports_simplified_chinese": False, "Tags": "B"},
        {"Name": "g5", "owners_mid": 1, "total_reviews": 1, "positive_rate": 1.0, "supports_simplified_chinese": False, "Tags": "B"},
        {"Name": "g6", "owners_mid": 1, "total_reviews": 1, "positive_rate": 1.0, "supports_simplified_chinese": False, "Tags": "C"},
    ])
    tbl = build_dashboard_tables(df, top_n=2)["tag_distribution"].set_index("tag")
    assert tbl.loc["A", "share"] == 3 / 6
    assert tbl.loc["B", "share"] == 2 / 6


def test_median_positive_rate_reviewed_excludes_no_review_rows():
    df = pd.DataFrame([
        {"review_signal": "low", "owners_mid": 1, "total_reviews": 0, "positive_rate": 0.0},
        {"review_signal": "low", "owners_mid": 1, "total_reviews": 10, "positive_rate": 0.9},
    ])
    tbl = build_dashboard_tables(df)["review_signal_distribution"].set_index("review_signal")
    assert tbl.loc["low", "median_positive_rate_reviewed"] == 0.9


def test_median_positive_rate_reviewed_nan_when_no_reviewed_rows():
    df = pd.DataFrame([
        {"review_signal": "low", "owners_mid": 1, "total_reviews": 0, "positive_rate": 0.0},
        {"review_signal": "low", "owners_mid": 1, "total_reviews": 0, "positive_rate": 0.0},
    ])
    tbl = build_dashboard_tables(df)["review_signal_distribution"].set_index("review_signal")
    assert pd.isna(tbl.loc["low", "median_positive_rate_reviewed"])
