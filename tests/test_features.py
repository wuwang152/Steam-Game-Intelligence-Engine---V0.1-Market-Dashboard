import pandas as pd
from steam_intelligence.features import add_engineered_features


def _minimal_base_df(**overrides):
    base = {
        "Release date": ["2020-01-01"],
        "Estimated owners": ["10,000 - 20,000"],
        "Positive": [80],
        "Negative": [20],
        "Price": [14.99],
        "Windows": [True],
        "Mac": [False],
        "Linux": [True],
        "Genres": ["Action;RPG"],
        "Tags": ["Indie;Singleplayer;Story Rich"],
        "Screenshots": ["a.jpg;b.jpg"],
        "Movies": ["trailer.mp4"],
    }
    base.update(overrides)
    return pd.DataFrame(base)


def test_feature_columns_exist():
    df = _minimal_base_df()
    out = add_engineered_features(df)

    expected = [
        "release_year", "owners_low", "owners_high", "owners_mid", "total_reviews",
        "positive_ratio", "review_signal", "review_sentiment", "price_bucket", "platform_count",
        "genre_count", "tag_count", "screenshot_count", "movie_count",
    ]
    for col in expected:
        assert col in out.columns

    assert out.loc[0, "release_year"] == 2020
    assert out.loc[0, "owners_mid"] == 15000
    assert out.loc[0, "total_reviews"] == 100
    assert out.loc[0, "platform_count"] == 2


def test_review_signal_categories_from_total_reviews():
    df = pd.DataFrame(
        {
            "Release date": ["2020-01-01"] * 5,
            "Estimated owners": ["10,000 - 20,000"] * 5,
            "Positive": [0, 1, 15, 80, 1200],
            "Negative": [0, 0, 10, 40, 300],
            "Price": [14.99] * 5,
            "Windows": [True] * 5,
            "Mac": [False] * 5,
            "Linux": [True] * 5,
            "Genres": ["Action;RPG"] * 5,
            "Tags": ["Indie;Singleplayer;Story Rich"] * 5,
            "Screenshots": ["a.jpg;b.jpg"] * 5,
            "Movies": ["trailer.mp4"] * 5,
        }
    )

    out = add_engineered_features(df)

    assert out.loc[0, "review_signal"] == "no_signal"   # 0
    assert out.loc[1, "review_signal"] == "very_low"    # 1
    assert out.loc[2, "review_signal"] == "low"         # 25
    assert out.loc[3, "review_signal"] == "medium"      # 120
    assert out.loc[4, "review_signal"] == "high"        # 1500


def test_zero_review_case_positive_ratio_safe():
    df = _minimal_base_df(Positive=[0], Negative=[0])
    out = add_engineered_features(df)

    assert out.loc[0, "total_reviews"] == 0
    assert out.loc[0, "positive_ratio"] == 0
    assert out.loc[0, "review_signal"] == "no_signal"
    assert out.loc[0, "review_sentiment"] == "weak"
