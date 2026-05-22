import streamlit as st

from app.utils import require_processed_data

st.title("Attention Distribution")
df = require_processed_data()
st.bar_chart(df["Peak CCU"].fillna(0).clip(upper=df["Peak CCU"].quantile(0.99)))
