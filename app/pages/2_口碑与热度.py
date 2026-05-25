import pandas as pd
import streamlit as st

from app.dashboard_table_loader import load_dashboard_table
from app.utils import REVIEW_SENTIMENT_LABELS, REVIEW_SIGNAL_LABELS, format_ranking_table_for_display, map_display_series, require_processed_data

GEN_CMD = "python scripts/generate_dashboard_tables.py --input data/processed/steam_games_cleaned.csv --output-dir data/processed/dashboard_tables --top-n 30 --min-reviews 20"


def _warn_missing(*tables: str) -> None:
    st.warning("未检测到对应后端聚合表，已切换到页面兜底逻辑。")
    st.caption(f"缺失表：{', '.join([f'{t}.csv' for t in tables])}")
    st.code(GEN_CMD, language="bash")


def _show_table(title: str, table_name: str, cols: list[str]) -> None:
    st.subheader(title)
    table = load_dashboard_table(table_name)
    if table is not None and not table.empty:
        st.dataframe(format_ranking_table_for_display(table[[c for c in cols if c in table.columns]]), use_container_width=True)
    else:
        _warn_missing(table_name)


st.title("口碑与热度")
df = require_processed_data()

st.subheader("评论热度信号")
signal = load_dashboard_table("review_signal_distribution")
if signal is not None and {"review_signal", "count"}.issubset(signal.columns):
    s = signal.copy()
    s["review_signal"] = map_display_series(s["review_signal"], REVIEW_SIGNAL_LABELS)
    st.bar_chart(s.set_index("review_signal")["count"])
    st.dataframe(format_ranking_table_for_display(s[[c for c in ["review_signal", "count", "share", "median_owners_mid", "median_positive_rate_reviewed"] if c in s.columns]]), use_container_width=True)
else:
    _warn_missing("review_signal_distribution")
    if "review_signal" in df.columns:
        st.bar_chart(map_display_series(df["review_signal"], REVIEW_SIGNAL_LABELS).value_counts())

st.subheader("口碑情绪分布")
sent = load_dashboard_table("review_sentiment_distribution")
if sent is not None and {"review_sentiment", "count"}.issubset(sent.columns):
    m = sent.copy()
    m["review_sentiment"] = map_display_series(m["review_sentiment"], REVIEW_SENTIMENT_LABELS)
    st.bar_chart(m.set_index("review_sentiment")["count"])
    st.dataframe(format_ranking_table_for_display(m[[c for c in ["review_sentiment", "count", "share", "median_owners_mid", "median_positive_rate_reviewed"] if c in m.columns]]), use_container_width=True)
else:
    _warn_missing("review_sentiment_distribution")

st.subheader("评论数区间与好评率中位数")
bucket = load_dashboard_table("review_bucket_positive_rate")
if bucket is not None and {"review_bucket", "count"}.issubset(bucket.columns):
    st.bar_chart(bucket.set_index("review_bucket")["count"])
    st.dataframe(format_ranking_table_for_display(bucket[[c for c in ["review_bucket", "count", "share", "median_positive_rate_reviewed"] if c in bucket.columns]]), use_container_width=True)
else:
    _warn_missing("review_bucket_positive_rate")
st.caption("好评率仅在有评论样本中更具解释意义。")

_show_table("评论数热门游戏", "top_games_by_reviews", ["AppID", "Name", "release_year", "price_bucket", "owners_mid", "total_reviews", "positive_rate", "supports_simplified_chinese", "Genres", "Tags"])
_show_table("高口碑游戏", "top_rated_games", ["AppID", "Name", "release_year", "price_bucket", "owners_mid", "total_reviews", "positive_rate", "supports_simplified_chinese", "Genres", "Tags"])
_show_table("高关注低口碑风险", "high_attention_low_rating", ["AppID", "Name", "release_year", "price_bucket", "owners_mid", "total_reviews", "positive_rate", "supports_simplified_chinese", "Genres", "Tags", "heuristic_reason"])
st.caption("机会识别榜单为透明启发式规则结果，不代表机器学习预测、因果结论或个性化推荐。")
