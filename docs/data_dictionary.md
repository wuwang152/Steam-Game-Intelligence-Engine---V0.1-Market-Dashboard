# Data Dictionary (V0.1)

## Core raw columns
- `AppID`: Steam application identifier.
- `Name`: Game title.
- `Release date`: Launch date.
- `Estimated owners`: Owner range text (e.g., `10,000 - 20,000`).
- `Price`: List price in USD.
- `Positive`, `Negative`: Review counts.
- `Genres`, `Tags`: Semicolon/comma-separated categorical text.
- `Screenshots`, `Movies`: Media URLs/identifiers.

## Engineered columns
- `release_year`: Parsed year from `Release date`.
- `owners_low`, `owners_high`: Parsed owner range bounds.
- `owners_mid`: Midpoint estimate for owners.
- `total_reviews`: `Positive + Negative`.
- `positive_ratio`: `Positive / total_reviews`.
- `review_signal`: Review volume band (`tiny`, `small`, `medium`, `large`).
- `review_sentiment`: Sentiment band from positive ratio (`weak`, `mixed`, `strong`).
- `price_bucket`: Price segment (`free`, `budget`, `mid`, `premium`, `luxury`).
- `platform_count`: Number of supported platforms across Windows/Mac/Linux.
- `genre_count`, `tag_count`, `screenshot_count`, `movie_count`: Parsed list counts.
