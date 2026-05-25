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
        "positive_rate", "positive_ratio", "review_log", "has_reviews", "is_free", "has_discount",
        "review_signal", "review_sentiment", "price_bucket", "platform_count",
        "genre_count", "tag_count", "screenshot_count", "movie_count",
        "has_valid_metascore", "has_valid_user_score", "has_peak_ccu", "has_recommendations",
        "has_playtime_forever", "has_recent_playtime", "has_genres", "has_tags", "has_categories",
        "has_developer", "has_publisher", "has_header_image", "has_screenshots", "has_about_text",
        "supported_language_count", "full_audio_language_count", "supports_simplified_chinese",
        "supports_english", "supports_japanese", "supports_korean", "has_chinese_audio",
    ]
    for col in expected:
        assert col in out.columns


def test_owner_range_parsing():
    df = pd.DataFrame({"Release date":["2020-01-01"],"Estimated owners":["10,000 - 20,000"],"Positive":[1],"Negative":[1],"Price":[0],"Windows":[True],"Mac":[False],"Linux":[False],"Genres":["Action"],"Tags":["Indie"],"Screenshots":[""],"Movies":[""]})
    out = add_engineered_features(df)
    assert out.loc[0, "owners_low"] == 10000
    assert out.loc[0, "owners_high"] == 20000
    assert out.loc[0, "owners_mid"] == 15000


def test_zero_review_handling_and_no_reviews_sentiment():
    df = pd.DataFrame({"Release date":["2021-01-01"],"Estimated owners":["0 - 0"],"Positive":[0],"Negative":[0],"Price":[5.99],"Windows":[True],"Mac":[True],"Linux":[False],"Genres":["Indie"],"Tags":["Singleplayer"],"Screenshots":[""],"Movies":[""]})
    out = add_engineered_features(df)
    assert out.loc[0, "total_reviews"] == 0
    assert out.loc[0, "positive_ratio"] == 0
    assert out.loc[0, "has_reviews"] == False
    assert out.loc[0, "review_signal"] == "no_signal"
    assert out.loc[0, "review_sentiment"] == "no_reviews"


def test_review_signal_bins():
    df = pd.DataFrame({"Release date":["2021-01-01"]*8,"Estimated owners":["0 - 0"]*8,"Positive":[0,1,19,20,99,100,999,1000],"Negative":[0]*8,"Price":[0]*8,"Windows":[True]*8,"Mac":[False]*8,"Linux":[False]*8,"Genres":["Action"]*8,"Tags":["Indie"]*8,"Screenshots":[""]*8,"Movies":[""]*8})
    out = add_engineered_features(df)
    assert list(out["review_signal"].astype(str)) == ["no_signal", "very_low", "very_low", "low", "low", "medium", "medium", "high"]


def test_review_sentiment_bins():
    df = pd.DataFrame({"Release date":["2021-01-01","2021-01-01","2021-01-01"],"Estimated owners":["0 - 0","0 - 0","0 - 0"],"Positive":[3,5,8],"Negative":[7,5,2],"Price":[0,0,0],"Windows":[True,True,True],"Mac":[False,False,False],"Linux":[False,False,False],"Genres":["Action","Action","Action"],"Tags":["Indie","Indie","Indie"],"Screenshots":["","",""] ,"Movies":["","",""]})
    out = add_engineered_features(df)
    assert list(out["review_sentiment"].astype(str)) == ["weak", "mixed", "strong"]


def test_item_counting():
    df = pd.DataFrame({"Release date":["2022-01-01"],"Estimated owners":["0 - 0"],"Positive":[1],"Negative":[1],"Price":[1.99],"Windows":[True],"Mac":[False],"Linux":[False],"Genres":["Action;RPG"],"Tags":["Indie;Singleplayer;Story Rich"],"Screenshots":["a.jpg;b.jpg"],"Movies":[""]})
    out = add_engineered_features(df)
    assert out.loc[0, "genre_count"] == 2
    assert out.loc[0, "tag_count"] == 3
    assert out.loc[0, "screenshot_count"] == 2
    assert out.loc[0, "movie_count"] == 0


def test_messy_owner_ranges_invalid_dates_and_numeric_parsing():
    df = pd.DataFrame({"Release date":["not-a-date",None],"Estimated owners":["0 - 20,000","20000 - 10000"],"Positive":["10",1],"Negative":["5",1],"Price":["USD 9.99","€0"],"Discount":["15%",0],"Windows":["yes",False],"Mac":["1",False],"Linux":["true",True]})
    out = add_engineered_features(df)
    assert pd.isna(out.loc[0, "release_year"]) and pd.isna(out.loc[1, "release_year"])
    assert out.loc[0, "owners_low"] == 0 and out.loc[0, "owners_high"] == 20000
    assert out.loc[1, "owners_low"] == 10000 and out.loc[1, "owners_high"] == 20000
    assert out.loc[0, "has_discount"] == True
    assert out.loc[0, "platform_count"] == 3
    assert str(out.loc[0, "price_bucket"]) == "budget"


def test_missing_optional_columns_safe_defaults():
    df = pd.DataFrame({"Release date": ["2020-01-01"], "Estimated owners": ["0 - 0"], "Positive": [0], "Negative": [0], "Price": [0]})
    out = add_engineered_features(df)
    false_flags = [
        "has_valid_metascore", "has_valid_user_score", "has_peak_ccu", "has_recommendations",
        "has_playtime_forever", "has_recent_playtime", "has_tags", "has_categories", "has_developer",
        "has_publisher", "has_header_image", "has_about_text", "supports_simplified_chinese",
        "supports_english", "supports_japanese", "supports_korean", "has_chinese_audio", "has_screenshots",
    ]
    for col in false_flags:
        assert out.loc[0, col] == False
    assert out.loc[0, "supported_language_count"] == 0
    assert out.loc[0, "full_audio_language_count"] == 0


def test_score_activity_language_and_metadata_flags():
    df = pd.DataFrame(
        {
            "Release date": ["2021-01-01", "2021-01-01", "2021-01-01", "2021-01-01"],
            "Estimated owners": ["0 - 0"] * 4,
            "Positive": [1] * 4,
            "Negative": [1] * 4,
            "Price": [1.0] * 4,
            "Metacritic score": [0, 85, 0, 85],
            "User score": [0, 0, 78, 78],
            "Peak CCU": [0, 100, 0, 0],
            "Recommendations": [0, 0, 50, 0],
            "Average playtime forever": [0, 10, 0, 0],
            "Median playtime forever": [0, 0, 20, 0],
            "Average playtime two weeks": [0, 0, 0, 30],
            "Median playtime two weeks": [0, 0, 10, 0],
            "Supported languages": [
                "English, Simplified Chinese, Japanese",
                "English; Chinese (Simplified); Korean",
                "简体中文, 英语",
                "",
            ],
            "Full audio languages": ["Simplified Chinese", "Chinese", "", None],
            "Genres": ["Action", " ", None, "RPG"],
            "Tags": ["Indie", "", None, "Action"],
            "Categories": ["Single-player", "", None, "Co-op"],
            "Developers": ["Valve", "", None, "N/A Dev"],
            "Publishers": ["Valve", "", None, "N/A Pub"],
            "Header image": ["http://img", "", None, "img2"],
            "About the game": ["Some text", "", None, "More text"],
            "Screenshots": ["a.jpg;b.jpg", "", None, "c.jpg"],
        }
    )
    out = add_engineered_features(df)

    assert out["has_valid_metascore"].tolist() == [False, True, False, True]
    assert out["has_valid_user_score"].tolist() == [False, False, True, True]
    assert out["has_peak_ccu"].tolist() == [False, True, False, False]
    assert out["has_recommendations"].tolist() == [False, False, True, False]
    assert out["has_playtime_forever"].tolist() == [False, True, True, False]
    assert out["has_recent_playtime"].tolist() == [False, False, True, True]

    assert out["supports_simplified_chinese"].tolist() == [True, True, True, False]
    assert out["supports_english"].tolist() == [True, True, True, False]
    assert out["supports_japanese"].tolist() == [True, False, False, False]
    assert out["supports_korean"].tolist() == [False, True, False, False]
    assert out["has_chinese_audio"].tolist() == [True, True, False, False]
    assert (out["supported_language_count"] >= 0).all()
    assert (out["full_audio_language_count"] >= 0).all()

    assert out["has_genres"].tolist() == [True, False, False, True]
    assert out["has_tags"].tolist() == [True, False, False, True]
    assert out["has_categories"].tolist() == [True, False, False, True]
    assert out["has_developer"].tolist() == [True, False, False, True]
    assert out["has_publisher"].tolist() == [True, False, False, True]
    assert out["has_header_image"].tolist() == [True, False, False, True]
    assert out["has_about_text"].tolist() == [True, False, False, True]
    assert out["has_screenshots"].tolist() == [True, False, False, True]


def test_placeholder_strings_are_treated_as_missing():
    df = pd.DataFrame(
        {
            "Release date": ["2021-01-01"],
            "Estimated owners": ["0 - 0"],
            "Positive": [1],
            "Negative": [1],
            "Price": [1.0],
            "Genres": ["None"],
            "Tags": ["None"],
            "Categories": ["N/A"],
            "Developers": ["nan"],
            "Publishers": ["null"],
            "Screenshots": ["None"],
            "About the game": ["None"],
            "Supported languages": ["None"],
            "Full audio languages": ["None"],
        }
    )

    out = add_engineered_features(df)

    assert out.loc[0, "has_genres"] == False
    assert out.loc[0, "genre_count"] == 0
    assert out.loc[0, "has_tags"] == False
    assert out.loc[0, "tag_count"] == 0
    assert out.loc[0, "has_categories"] == False
    assert out.loc[0, "has_developer"] == False
    assert out.loc[0, "has_publisher"] == False
    assert out.loc[0, "screenshot_count"] == 0
    assert out.loc[0, "has_screenshots"] == False
    assert out.loc[0, "has_about_text"] == False
    assert out.loc[0, "supported_language_count"] == 0
    assert out.loc[0, "supports_simplified_chinese"] == False
    assert out.loc[0, "supports_english"] == False
    assert out.loc[0, "supports_japanese"] == False
    assert out.loc[0, "supports_korean"] == False
    assert out.loc[0, "full_audio_language_count"] == 0
    assert out.loc[0, "has_chinese_audio"] == False
