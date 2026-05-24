import pandas as pd
from steam_intelligence.features import add_engineered_features


def test_v02_feature_columns_exist_and_core_values():
    df = pd.DataFrame(
        {
            "Release date": ["2020-01-01"],
            "Estimated owners": ["10,000 - 20,000"],
            "Positive": [80],
            "Negative": [20],
            "Price": [14.99],
            "Discount": [10],
            "Windows": [True],
            "Mac": [False],
            "Linux": [True],
            "Genres": ["Action;RPG"],
            "Tags": ["Indie;Singleplayer;Story Rich"],
            "Screenshots": ["a.jpg;b.jpg"],
            "Movies": ["trailer.mp4"],
        }
    )
    out = add_engineered_features(df)

    expected = [
        "release_year", "owners_low", "owners_high", "owners_mid", "total_reviews",
        "positive_rate", "positive_ratio", "review_log", "is_free", "has_discount",
        "price_bucket", "platform_count", "genre_count", "tag_count", "screenshot_count", "movie_count",
    ]
    for col in expected:
        assert col in out.columns

    assert out.loc[0, "release_year"] == 2020
    assert out.loc[0, "owners_mid"] == 15000
    assert out.loc[0, "total_reviews"] == 100
    assert out.loc[0, "positive_rate"] == 0.8
    assert out.loc[0, "has_discount"]
    assert out.loc[0, "platform_count"] == 2


def test_zero_and_missing_reviews_are_safe():
    df = pd.DataFrame(
        {
            "Release date": ["2021-01-01", "2021-01-01"],
            "Estimated owners": ["0 - 0", "0 - 0"],
            "Positive": [0, None],
            "Negative": [0, None],
            "Price": [0, 2.99],
            "Discount": [0, 0],
            "Windows": [True, True],
            "Mac": [False, False],
            "Linux": [False, False],
        }
    )
    out = add_engineered_features(df)

    assert (out["total_reviews"] == 0).all()
    assert (out["positive_rate"] == 0).all()
    assert (out["review_log"] == 0).all()


def test_messy_owner_ranges_and_invalid_release_dates():
    df = pd.DataFrame(
        {
            "Release date": ["not-a-date", None],
            "Estimated owners": ["0 - 20,000", "20000 - 10000"],
            "Positive": [1, 1],
            "Negative": [1, 1],
            "Price": [0, 0],
            "Discount": [0, 0],
            "Windows": [True, False],
            "Mac": [False, False],
            "Linux": [False, True],
        }
    )
    out = add_engineered_features(df)

    assert pd.isna(out.loc[0, "release_year"])
    assert pd.isna(out.loc[1, "release_year"])
    assert out.loc[0, "owners_low"] == 0
    assert out.loc[0, "owners_high"] == 20000
    assert out.loc[1, "owners_low"] == 10000
    assert out.loc[1, "owners_high"] == 20000


def test_free_discount_and_multiplatform_string_inputs():
    df = pd.DataFrame(
        {
            "Release date": ["2022-01-01"],
            "Estimated owners": ["0 - 0"],
            "Positive": ["10"],
            "Negative": ["5"],
            "Price": ["0"],
            "Discount": ["15"],
            "Windows": ["yes"],
            "Mac": ["1"],
            "Linux": ["true"],
        }
    )
    out = add_engineered_features(df)

    assert out.loc[0, "is_free"]
    assert out.loc[0, "has_discount"]
    assert out.loc[0, "platform_count"] == 3
    assert str(out.loc[0, "price_bucket"]) == "Free"
