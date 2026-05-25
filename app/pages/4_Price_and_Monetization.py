import streamlit as st

from app.utils import PRICE_BUCKET_LABELS, get_available_columns, map_display_series, rename_display_columns, require_processed_data

PRICE_BUCKET_ORDER = ["free", "budget", "mid", "premium", "luxury"]

st.title("价格与变现")
df = require_processed_data()

if "price_bucket" in df.columns:
    st.subheader("价格分层分布")
    bucket_series = map_display_series(df["price_bucket"], PRICE_BUCKET_LABELS)
    ordered = [x for x in PRICE_BUCKET_ORDER if x in bucket_series.unique()]
    remainder = sorted([x for x in bucket_series.unique() if x not in ordered])
    st.bar_chart(bucket_series.value_counts().reindex(ordered + remainder, fill_value=0))

if "Price" in df.columns:
    st.subheader("免费与付费占比")
    free_paid = df["Price"].fillna(0).apply(lambda x: "免费" if x == 0 else "付费").value_counts()
    st.bar_chart(free_paid)

if "price_bucket" in df.columns and "total_reviews" in df.columns:
    st.subheader("各价格分层评论数中位数")
    median_reviews = df.groupby("price_bucket", dropna=True)["total_reviews"].median()
    order = [x for x in PRICE_BUCKET_ORDER if x in median_reviews.index]
    remainder = [x for x in median_reviews.index if x not in order]
    median_reviews = median_reviews.reindex(order + sorted(remainder))
    display_reviews = median_reviews.copy()
    display_reviews.index = [PRICE_BUCKET_LABELS.get(str(x), str(x)) for x in display_reviews.index]
    st.bar_chart(display_reviews)

st.subheader("价格与变现表")
table_cols = get_available_columns(df, ["Name", "Price", "Discount", "DLC count", "price_bucket"])
if table_cols:
    display_df = df[table_cols].head(250).copy()
    if "price_bucket" in display_df.columns:
        display_df["price_bucket"] = map_display_series(display_df["price_bucket"], PRICE_BUCKET_LABELS)
    st.dataframe(rename_display_columns(display_df), use_container_width=True)
else:
    st.info("缺少可展示的价格或变现相关列。")
