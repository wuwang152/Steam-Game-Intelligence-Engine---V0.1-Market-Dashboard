import streamlit as st

from app.utils import require_processed_data

st.title("Release Dynamics")
df = require_processed_data()

if "release_year" not in df.columns or not df["release_year"].notna().any():
    st.warning("The dataset does not include release_year values, so release trend charts are unavailable.")
    st.stop()

release_counts = df.groupby("release_year", dropna=True).size().rename("games").sort_index()
st.subheader("Games Released by Year")
st.caption("This shows how many games were released each year in the processed dataset.")
st.caption("Recent and future release years may be incomplete.")
st.line_chart(release_counts)

if "Price" in df.columns:
    yearly_price = df.groupby("release_year", dropna=True)["Price"].median().dropna().sort_index()
    if not yearly_price.empty:
        st.subheader("Median Price by Year")
        st.caption("This line highlights long-term shifts in launch pricing over time.")
        st.line_chart(yearly_price)

if "positive_ratio" in df.columns:
    yearly_ratio = df.groupby("release_year", dropna=True)["positive_ratio"].median().dropna().sort_index()
    if not yearly_ratio.empty:
        st.subheader("Median Positive Rate by Year")
        st.caption("This line summarizes how median player sentiment changed by release year.")
        st.caption("Positive Rate is most meaningful for games with reviews.")
        st.line_chart(yearly_ratio)
