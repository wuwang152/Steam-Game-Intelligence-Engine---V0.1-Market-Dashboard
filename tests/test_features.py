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
        "positive_ratio", "review_signal", "review_sentiment", "price_bucket", "platform_count", "genre_count",
        "tag_count", "screenshot_count", "movie_count",
    ]
    for col in expected:
        assert col in out.columns

    assert out.loc[0, "release_year"] == 2020
    assert out.loc[0, "owners_mid"] == 15000
    assert out.loc[0, "total_reviews"] == 100
    assert out.loc[0, "platform_count"] == 2
