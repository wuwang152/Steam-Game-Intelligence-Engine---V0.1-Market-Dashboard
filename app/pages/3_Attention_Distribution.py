import streamlit as st
from app.utils import require_data_page

df = require_data_page("Attention Distribution")
if df is not None and "Peak CCU" in df.columns:
    st.bar_chart(df["Peak CCU"].fillna(0).clip(upper=df["Peak CCU"].quantile(0.99)))
else:
    st.info("Missing required column: Peak CCU")
