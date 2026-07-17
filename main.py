import streamlit as st

from dashboard import show_dashboard
from config import APP_NAME, MARKETS

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📈",
    layout="wide"
)

st.sidebar.title("📊 Market Selection")

market = st.sidebar.selectbox(
    "Select a Volatility Index",
    MARKETS
)

st.sidebar.success(f"Selected Market: {market}")

show_dashboard()
