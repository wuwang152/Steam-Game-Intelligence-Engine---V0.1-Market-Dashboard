import pandas as pd

from steam_intelligence.reporting import (
    build_markdown_table,
    compute_metrics,
    generate_hidden_gems,
    prepare_rank_table,
)


def _base_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Name": ["A", "B", "C", "D"],
            "release_year": [2020, 2021, None, 2021],
            "owners_mid": [1000, 2000, None, 1200],
            "total_reviews": [0, 100, 30, 25],
            "positive_rate": [0.0, 0.9, 0.88, 0.86],
            "review_log": [0.0, 4.6, 3.4, 3.2],
            "has_reviews": [False, True, True, True],
            "is_free": [True, False, False, True],
            "has_discount": [False, True, False, False],
            "platform_count": [1, 3, 2, 1],
            "price_bucket": ["free", "premium", "budget", "free"],
            "review_signal": ["no_signal", "medium", "low", "low"],
            "review_sentiment": ["no_reviews", "strong", "strong", "strong"],
        }
    )


def test_compute_metrics_basic_and_zero_reviews():
    metrics = compute_metrics(_base_df())
    assert metrics["total_games"] == 4
    assert metrics["games_with_reviews"] == 3
    assert round(metrics["share_with_reviews"], 2) == 0.75
    assert metrics["median_positive_rate_reviewed"] == 0.88


def test_missing_values_do_not_crash_rank_table():
    df = _base_df()
    table = prepare_rank_table(df, ["owners_mid", "total_reviews"], [False, False], limit=3)
    assert not table.empty
    assert len(table) == 3


def test_hidden_gems_logic():
    gems = generate_hidden_gems(_base_df())
    assert not gems.empty
    # Candidate set owners_mid: 2000, nan, 1200 -> median 1600 => only D qualifies with known owners_mid <= 1600
    assert "D" in gems["Name"].tolist()


def test_markdown_table_formatting():
    md = build_markdown_table(pd.DataFrame({"A": ["x"], "B": ["y"]}))
    assert "| A | B |" in md
    assert "| x | y |" in md
