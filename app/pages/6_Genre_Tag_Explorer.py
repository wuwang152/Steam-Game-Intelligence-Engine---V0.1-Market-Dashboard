import streamlit as st

from app.utils import get_available_columns, require_processed_data, top_split_values

st.title("Genre/Tag Explorer")
df = require_processed_data()

st.sidebar.header("Genre/Tag Controls")
top_n = st.sidebar.slider("Top N values", min_value=5, max_value=50, value=20, step=5)

if "tag_count" in df.columns and df["tag_count"].notna().any():
    max_tag_count = int(df["tag_count"].max())
    min_tags = st.sidebar.slider("Minimum tag_count", min_value=0, max_value=max_tag_count, value=0)
    filtered_df = df[df["tag_count"].fillna(0) >= min_tags].copy()
else:
    filtered_df = df.copy()

st.subheader("Top Genres")
genre_counts = top_split_values(filtered_df, "Genres", sep=";", top_n=top_n)
if not genre_counts.empty:
    st.bar_chart(genre_counts)
else:
    st.info("Genres column is missing or empty.")

st.subheader("Top Tags")
tag_counts = top_split_values(filtered_df, "Tags", sep=";", top_n=top_n)
if not tag_counts.empty:
    st.bar_chart(tag_counts)
else:
    st.info("Tags column is missing or empty.")

st.subheader("Filtered Games Table")
table_cols = get_available_columns(filtered_df, ["Name", "Genres", "Tags", "genre_count", "tag_count", "positive_ratio"])
if table_cols:
    st.dataframe(filtered_df[table_cols].head(300), use_container_width=True)
else:
    st.info("No standard genre/tag table columns are available.")
