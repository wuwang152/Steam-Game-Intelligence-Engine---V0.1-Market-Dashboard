import pandas as pd
from steam_intelligence.features import add_engineered_features


def test_feature_columns_exist():
    df = pd.DataFrame(
        {
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
    )
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


def test_owner_range_parsing():
    df = pd.DataFrame(
        {
            "Release date": ["2020-01-01"],
            "Estimated owners": ["10,000 - 20,000"],
            "Positive": [1],
            "Negative": [1],
            "Price": [0],
            "Windows": [True],
            "Mac": [False],
            "Linux": [False],
            "Genres": ["Action"],
            "Tags": ["Indie"],
            "Screenshots": [""],
            "Movies": [""],
        }
    )
    out = add_engineered_features(df)

    assert out.loc[0, "owners_low"] == 10000
    assert out.loc[0, "owners_high"] == 20000
    assert out.loc[0, "owners_mid"] == 15000


def test_zero_review_handling():
    df = pd.DataFrame(
        {
            "Release date": ["2021-01-01"],
            "Estimated owners": ["0 - 0"],
            "Positive": [0],
            "Negative": [0],
            "Price": [5.99],
            "Windows": [True],
            "Mac": [True],
            "Linux": [False],
            "Genres": ["Indie"],
            "Tags": ["Singleplayer"],
            "Screenshots": [""],
            "Movies": [""],
        }
    )
    out = add_engineered_features(df)

    assert out.loc[0, "total_reviews"] == 0
    assert out.loc[0, "positive_ratio"] == 0
    assert out.loc[0, "review_signal"] == "no_signal"


def test_review_signal_bins():
    df = pd.DataFrame(
        {
            "Release date": ["2021-01-01"] * 8,
            "Estimated owners": ["0 - 0"] * 8,
            "Positive": [0, 1, 19, 20, 99, 100, 999, 1000],
            "Negative": [0] * 8,
            "Price": [0] * 8,
            "Windows": [True] * 8,
            "Mac": [False] * 8,
            "Linux": [False] * 8,
            "Genres": ["Action"] * 8,
            "Tags": ["Indie"] * 8,
            "Screenshots": [""] * 8,
            "Movies": [""] * 8,
        }
    )
    out = add_engineered_features(df)

    assert list(out["review_signal"].astype(str)) == [
        "no_signal", "very_low", "very_low", "low", "low", "medium", "medium", "high"
    ]


def test_review_sentiment_bins():
    df = pd.DataFrame(
        {
            "Release date": ["2021-01-01", "2021-01-01", "2021-01-01"],
            "Estimated owners": ["0 - 0", "0 - 0", "0 - 0"],
            "Positive": [3, 5, 8],
            "Negative": [7, 5, 2],
            "Price": [0, 0, 0],
            "Windows": [True, True, True],
            "Mac": [False, False, False],
            "Linux": [False, False, False],
            "Genres": ["Action", "Action", "Action"],
            "Tags": ["Indie", "Indie", "Indie"],
            "Screenshots": ["", "", ""],
            "Movies": ["", "", ""],
        }
    )
    out = add_engineered_features(df)

    assert list(out["review_sentiment"].astype(str)) == ["weak", "mixed", "strong"]


def test_item_counting():
    df = pd.DataFrame(
        {
            "Release date": ["2022-01-01"],
            "Estimated owners": ["0 - 0"],
            "Positive": [1],
            "Negative": [1],
            "Price": [1.99],
            "Windows": [True],
            "Mac": [False],
            "Linux": [False],
            "Genres": ["Action;RPG"],
            "Tags": ["Indie;Singleplayer;Story Rich"],
            "Screenshots": ["a.jpg;b.jpg"],
            "Movies": [""],
        }
    )
    out = add_engineered_features(df)

    assert out.loc[0, "genre_count"] == 2
    assert out.loc[0, "tag_count"] == 3
    assert out.loc[0, "screenshot_count"] == 2
    assert out.loc[0, "movie_count"] == 0
