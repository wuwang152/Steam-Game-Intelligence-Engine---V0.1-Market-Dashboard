"""Build dashboard-ready aggregation and heuristic ranking tables."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

MISSING_TEXT_TOKENS = {"", "none", "nan", "null", "n/a", "na", "[]", "-"}

TABLE_COLUMNS: dict[str, list[str]] = {
    "summary_metrics": [
        "total_games", "games_with_reviews", "share_with_reviews", "median_owners_mid", "median_total_reviews",
        "median_positive_rate_reviewed", "free_share", "discount_share", "simplified_chinese_support_share",
        "english_support_share", "japanese_support_share", "korean_support_share", "games_with_tags",
        "games_with_categories", "games_with_developer", "games_with_publisher",
    ],
    "yearly_release_counts": ["release_year", "count", "share"],
    "price_bucket_distribution": ["price_bucket", "count", "share", "median_owners_mid", "median_total_reviews", "median_positive_rate_reviewed"],
    "owners_tier_distribution": ["owners_tier", "count", "share", "median_positive_rate_reviewed", "median_total_reviews"],
    "platform_count_distribution": ["platform_count", "count", "share"],
    "review_signal_distribution": ["review_signal", "count", "share", "median_owners_mid", "median_positive_rate_reviewed"],
    "review_sentiment_distribution": ["review_sentiment", "count", "share", "median_owners_mid", "median_total_reviews"],
    "review_bucket_positive_rate": ["review_bucket", "count", "share", "median_positive_rate_reviewed", "median_owners_mid"],
    "genre_distribution": ["genre", "count", "share", "median_owners_mid", "median_total_reviews", "median_positive_rate_reviewed", "simplified_chinese_support_share"],
    "tag_distribution": ["tag", "count", "share", "median_owners_mid", "median_total_reviews", "median_positive_rate_reviewed", "simplified_chinese_support_share"],
    "category_distribution": ["category", "count", "share", "median_owners_mid", "median_total_reviews", "median_positive_rate_reviewed"],
    "language_support_summary": ["language", "count", "share"],
    "localization_by_genre": ["genre", "count", "simplified_chinese_support_share", "english_support_share", "japanese_support_share", "korean_support_share", "median_positive_rate_reviewed", "median_total_reviews"],
}

RANKING_COLUMNS = ["AppID", "Name", "release_year", "price_bucket", "owners_mid", "total_reviews", "positive_rate", "supports_simplified_chinese", "Genres", "Tags"]


def _empty(name: str) -> pd.DataFrame:
    if name in TABLE_COLUMNS:
        return pd.DataFrame(columns=TABLE_COLUMNS[name])
    return pd.DataFrame(columns=RANKING_COLUMNS)


def safe_numeric(df: pd.DataFrame, column: str, default: float = np.nan) -> pd.Series:
    if column not in df.columns:
        return pd.Series(default, index=df.index, dtype=float)
    cleaned = (df[column].astype(str).str.replace(",", "", regex=False).str.replace(r"[^0-9.\-]", "", regex=True).str.strip())
    cleaned = cleaned.replace({"": np.nan, "none": np.nan, "nan": np.nan, "null": np.nan})
    out = pd.to_numeric(cleaned, errors="coerce")
    return out if np.isnan(default) else out.fillna(default)


def safe_bool(df: pd.DataFrame, column: str, default: bool = False) -> pd.Series:
    if column not in df.columns:
        return pd.Series(default, index=df.index, dtype=bool)
    s = df[column]
    return s.map(lambda v: (str(v).strip().lower() in {"true", "1", "yes", "y", "t"}) if not pd.isna(v) else default)


def clean_text_value(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if text.lower() in MISSING_TEXT_TOKENS:
        return None
    return text


def split_list_values(series: pd.Series) -> pd.Series:
    items: list[str] = []
    for value in series:
        cleaned = clean_text_value(value)
        if cleaned is None:
            continue
        parts = [clean_text_value(x) for x in re.split(r"[;,]", cleaned)]
        items.extend([x for x in parts if x is not None])
    return pd.Series(items, dtype=object)


def distribution_table(series: pd.Series, category_col: str) -> pd.DataFrame:
    cleaned = series.map(clean_text_value).dropna()
    if cleaned.empty:
        return pd.DataFrame(columns=[category_col, "count", "share"])
    counts = cleaned.value_counts(dropna=False).rename_axis(category_col).reset_index(name="count")
    counts["share"] = counts["count"] / counts["count"].sum()
    return counts


def grouped_metric_table(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    if group_col not in df.columns:
        return pd.DataFrame(columns=[group_col, "count", "share", "median_owners_mid", "median_total_reviews", "median_positive_rate_reviewed"])
    gdf = df[[group_col, "owners_mid", "total_reviews", "positive_rate"]].copy()
    gdf[group_col] = gdf[group_col].map(clean_text_value)
    gdf = gdf.dropna(subset=[group_col])
    if gdf.empty:
        return pd.DataFrame(columns=[group_col, "count", "share", "median_owners_mid", "median_total_reviews", "median_positive_rate_reviewed"])
    out = gdf.groupby(group_col, dropna=False).agg(
        count=(group_col, "size"),
        median_owners_mid=("owners_mid", "median"),
        median_total_reviews=("total_reviews", "median"),
        median_positive_rate_reviewed=("positive_rate", "median"),
    ).reset_index()
    out["share"] = out["count"] / out["count"].sum()
    return out[[group_col, "count", "share", "median_owners_mid", "median_total_reviews", "median_positive_rate_reviewed"]]


def _list_table(df: pd.DataFrame, source_col: str, out_col: str, top_n: int, include_lang_share: bool = True) -> pd.DataFrame:
    if source_col not in df.columns:
        return _empty(f"{out_col}_distribution")
    rows = []
    for _, row in df.iterrows():
        cleaned = clean_text_value(row[source_col])
        if cleaned is None:
            continue
        for part in [clean_text_value(x) for x in re.split(r"[;,]", cleaned)]:
            if part is None:
                continue
            rows.append({out_col: part, "owners_mid": row["owners_mid"], "total_reviews": row["total_reviews"], "positive_rate": row["positive_rate"], "supports_simplified_chinese": row["supports_simplified_chinese"]})
    if not rows:
        return _empty(f"{out_col}_distribution")
    out = pd.DataFrame(rows)
    tbl = out.groupby(out_col).agg(
        count=(out_col, "size"),
        median_owners_mid=("owners_mid", "median"),
        median_total_reviews=("total_reviews", "median"),
        median_positive_rate_reviewed=("positive_rate", "median"),
        simplified_chinese_support_share=("supports_simplified_chinese", "mean"),
    ).reset_index().sort_values("count", ascending=False).head(top_n)
    tbl["share"] = tbl["count"] / tbl["count"].sum()
    base_cols = [out_col, "count", "share", "median_owners_mid", "median_total_reviews", "median_positive_rate_reviewed"]
    return tbl[base_cols + (["simplified_chinese_support_share"] if include_lang_share else [])]


def build_dashboard_tables(df: pd.DataFrame, top_n: int = 30, min_reviews: int = 20) -> dict[str, pd.DataFrame]:
    data = df.copy(deep=True)
    data["owners_mid"] = safe_numeric(data, "owners_mid")
    data["total_reviews"] = safe_numeric(data, "total_reviews", 0)
    data["positive_rate"] = safe_numeric(data, "positive_rate", 0)
    data["release_year"] = safe_numeric(data, "release_year")
    data["platform_count"] = safe_numeric(data, "platform_count", 0)
    data["supports_simplified_chinese"] = safe_bool(data, "supports_simplified_chinese")
    data["supports_english"] = safe_bool(data, "supports_english")
    data["supports_japanese"] = safe_bool(data, "supports_japanese")
    data["supports_korean"] = safe_bool(data, "supports_korean")
    data["has_chinese_audio"] = safe_bool(data, "has_chinese_audio")
    data["has_discount"] = safe_bool(data, "has_discount")
    data["is_free"] = safe_bool(data, "is_free")

    tables = {}
    reviewed = data[data["total_reviews"] > 0]
    tables["summary_metrics"] = pd.DataFrame([{
        "total_games": len(data), "games_with_reviews": len(reviewed), "share_with_reviews": len(reviewed) / len(data) if len(data) else np.nan,
        "median_owners_mid": data["owners_mid"].median(), "median_total_reviews": data["total_reviews"].median(),
        "median_positive_rate_reviewed": reviewed["positive_rate"].median(), "free_share": data["is_free"].mean(), "discount_share": data["has_discount"].mean(),
        "simplified_chinese_support_share": data["supports_simplified_chinese"].mean(), "english_support_share": data["supports_english"].mean(),
        "japanese_support_share": data["supports_japanese"].mean(), "korean_support_share": data["supports_korean"].mean(),
        "games_with_tags": data.get("Tags", pd.Series(index=data.index)).map(clean_text_value).notna().sum(),
        "games_with_categories": data.get("Categories", pd.Series(index=data.index)).map(clean_text_value).notna().sum(),
        "games_with_developer": data.get("Developers", pd.Series(index=data.index)).map(clean_text_value).notna().sum(),
        "games_with_publisher": data.get("Publishers", pd.Series(index=data.index)).map(clean_text_value).notna().sum(),
    }])[TABLE_COLUMNS["summary_metrics"]]

    tables["yearly_release_counts"] = distribution_table(data["release_year"], "release_year")
    tables["price_bucket_distribution"] = grouped_metric_table(data, "price_bucket")
    tables["price_bucket_distribution"] = tables["price_bucket_distribution"].rename(columns={"price_bucket":"price_bucket"})

    bins = [-np.inf, 0, 1e4, 5e4, 1e5, 5e5, 1e6, 1e7, np.inf]
    labels = ["0", "1–10k", "10k–50k", "50k–100k", "100k–500k", "500k–1M", "1M–10M", "10M+"]
    data["owners_tier"] = pd.cut(data["owners_mid"], bins=bins, labels=labels, include_lowest=True)
    ot = data.groupby("owners_tier", observed=False).agg(count=("owners_tier", "size"), median_positive_rate_reviewed=("positive_rate", "median"), median_total_reviews=("total_reviews", "median")).reset_index()
    ot["share"] = ot["count"] / ot["count"].sum() if ot["count"].sum() else np.nan
    tables["owners_tier_distribution"] = ot[TABLE_COLUMNS["owners_tier_distribution"]]

    tables["platform_count_distribution"] = distribution_table(data["platform_count"], "platform_count")
    tables["review_signal_distribution"] = grouped_metric_table(data, "review_signal")[["review_signal", "count", "share", "median_owners_mid", "median_positive_rate_reviewed"]]
    tables["review_sentiment_distribution"] = grouped_metric_table(data, "review_sentiment")[["review_sentiment", "count", "share", "median_owners_mid", "median_total_reviews"]]

    rb_bins = [-0.1, 0, 19, 99, 499, 999, 4999, 9999, 49999, np.inf]
    rb_labels = ["0", "1–19", "20–99", "100–499", "500–999", "1k–4,999", "5k–9,999", "10k–49,999", "50k+"]
    data["review_bucket"] = pd.cut(data["total_reviews"], bins=rb_bins, labels=rb_labels)
    rb = data.groupby("review_bucket", observed=False).agg(count=("review_bucket", "size"), median_positive_rate_reviewed=("positive_rate", "median"), median_owners_mid=("owners_mid", "median")).reset_index()
    rb["share"] = rb["count"] / rb["count"].sum() if rb["count"].sum() else np.nan
    tables["review_bucket_positive_rate"] = rb[TABLE_COLUMNS["review_bucket_positive_rate"]]

    tables["genre_distribution"] = _list_table(data, "Genres", "genre", top_n, True)
    tables["tag_distribution"] = _list_table(data, "Tags", "tag", top_n, True)
    tables["category_distribution"] = _list_table(data, "Categories", "category", top_n, False)

    lang_rows = []
    for key, col in [("simplified_chinese", "supports_simplified_chinese"), ("english", "supports_english"), ("japanese", "supports_japanese"), ("korean", "supports_korean"), ("chinese_audio", "has_chinese_audio")]:
        lang_rows.append({"language": key, "count": int(data[col].sum()), "share": float(data[col].mean()) if len(data) else np.nan})
    tables["language_support_summary"] = pd.DataFrame(lang_rows)

    lg = tables["genre_distribution"]["genre"].head(top_n).tolist() if not tables["genre_distribution"].empty else []
    if lg and "Genres" in data.columns:
        rows=[]
        for _, r in data.iterrows():
            cv=clean_text_value(r["Genres"])
            if cv is None: continue
            for g in [clean_text_value(x) for x in re.split(r"[;,]", cv)]:
                if g in lg:
                    rows.append({"genre":g, "supports_simplified_chinese":r["supports_simplified_chinese"], "supports_english":r["supports_english"], "supports_japanese":r["supports_japanese"], "supports_korean":r["supports_korean"], "positive_rate":r["positive_rate"], "total_reviews":r["total_reviews"]})
        if rows:
            ldf=pd.DataFrame(rows).groupby("genre").agg(count=("genre","size"), simplified_chinese_support_share=("supports_simplified_chinese","mean"), english_support_share=("supports_english","mean"), japanese_support_share=("supports_japanese","mean"), korean_support_share=("supports_korean","mean"), median_positive_rate_reviewed=("positive_rate","median"), median_total_reviews=("total_reviews","median")).reset_index().sort_values("count", ascending=False).head(top_n)
            tables["localization_by_genre"]=ldf[TABLE_COLUMNS["localization_by_genre"]]
        else: tables["localization_by_genre"]=_empty("localization_by_genre")
    else:
        tables["localization_by_genre"]=_empty("localization_by_genre")

    def rank(df0, name, sort_cols, asc, flt=None, note=None):
        cols = RANKING_COLUMNS + (["heuristic_reason"] if note else [])
        req = ["owners_mid", "total_reviews", "positive_rate"]
        if not set(req).issubset(data.columns):
            return pd.DataFrame(columns=cols)
        r = df0.copy()
        if flt is not None:
            r = r[flt(r)]
        if note is not None:
            r = r.assign(heuristic_reason=note)
        r = r.sort_values(sort_cols, ascending=asc).head(top_n)
        for c in RANKING_COLUMNS:
            if c not in r.columns:
                r[c] = np.nan
        return r[cols]

    tables["top_games_by_owners"] = rank(data, "top_games_by_owners", ["owners_mid", "total_reviews"], [False, False])
    tables["top_games_by_reviews"] = rank(data, "top_games_by_reviews", ["total_reviews", "owners_mid"], [False, False])
    tables["top_rated_games"] = rank(data, "top_rated_games", ["positive_rate", "total_reviews"], [False, False], lambda r: r["total_reviews"] >= min_reviews)
    tables["hidden_gems"] = rank(data, "hidden_gems", ["positive_rate", "total_reviews"], [False, False], lambda r: (r["total_reviews"] >= min_reviews) & (r["positive_rate"] >= 0.85) & (r["owners_mid"] <= r.loc[(r["total_reviews"] >= min_reviews) & (r["positive_rate"] >= 0.85), "owners_mid"].median()), "high_rating_low_estimated_ownership")
    tables["low_price_high_rating"] = rank(data, "low_price_high_rating", ["positive_rate", "total_reviews"], [False, False], lambda r: r.get("price_bucket", pd.Series(index=r.index)).isin(["free", "budget"]) & (r["total_reviews"] >= min_reviews) & (r["positive_rate"] >= 0.85), "low_price_high_rating")
    q75 = data["total_reviews"].quantile(0.75)
    tables["high_attention_low_rating"] = rank(data, "high_attention_low_rating", ["total_reviews", "positive_rate"], [False, True], lambda r: (r["total_reviews"] >= max(min_reviews, q75)) & (r["positive_rate"] < 0.70), "high_attention_low_rating")
    tables["chinese_supported_potential"] = rank(data, "chinese_supported_potential", ["positive_rate", "total_reviews"], [False, False], lambda r: (r["supports_simplified_chinese"]) & (r["total_reviews"] >= min_reviews) & (r["positive_rate"] >= 0.80) & (r["owners_mid"] <= r.loc[(r["supports_simplified_chinese"]) & (r["total_reviews"] >= min_reviews) & (r["positive_rate"] >= 0.80), "owners_mid"].median()), "chinese_supported_high_rating_low_exposure")
    reviewed_median = data.loc[data["total_reviews"] >= min_reviews, "owners_mid"].median()
    tables["localization_opportunities"] = rank(data, "localization_opportunities", ["positive_rate", "owners_mid"], [False, False], lambda r: (~r["supports_simplified_chinese"]) & (r["total_reviews"] >= min_reviews) & (r["positive_rate"] >= 0.85) & (r["owners_mid"] >= reviewed_median), "missing_simplified_chinese_high_rating_attention")
    return tables


def write_dashboard_tables(tables: dict[str, pd.DataFrame], output_dir: str | Path) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(out / f"{name}.csv", index=False)
