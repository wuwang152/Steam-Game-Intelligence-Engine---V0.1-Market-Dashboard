# Data Dictionary (V0.1)

## Core identifiers
- **AppID**: Unique Steam application identifier.
- **Name**: Game title.

## Release and ownership
- **Release date**: Original release date string from source data.
- **release_year**: Parsed release year used for time-series analysis.
- **Estimated owners**: Raw owner range string.
- **owners_low**: Lower bound of parsed owner range.
- **owners_high**: Upper bound of parsed owner range.
- **owners_mid**: Midpoint between owner range bounds.

## Pricing and monetization
- **Price**: Base price in USD.
- **Discount**: Discount percentage.
- **DLC count**: Number of downloadable content packs.
- **price_bucket**: Engineered categorical segment (free, budget, mid, premium, luxury).

## Reviews and reputation
- **Positive**: Count of positive reviews.
- **Negative**: Count of negative reviews.
- **total_reviews**: Positive + Negative review count.
- **positive_ratio**: Positive reviews divided by total reviews.
- **review_signal**: Categorical signal based on review volume tiers.
- **review_sentiment**: Categorical sentiment based on positive_ratio.

## Platforms and content richness
- **Windows/Mac/Linux**: Platform support flags.
- **platform_count**: Number of supported platforms.
- **Genres/Tags**: Raw semicolon/comma separated metadata.
- **genre_count/tag_count**: Parsed counts for genres and tags.
- **Screenshots/Movies**: Media references from source data.
- **screenshot_count/movie_count**: Parsed counts of screenshots and trailers.
