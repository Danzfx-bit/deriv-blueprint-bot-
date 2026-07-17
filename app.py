import streamlit as st

from dashboard import show_dashboard
from matches_differs import show as show_matches
from config import APP_NAME, MARKETS

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("NUTEC Blueprint AI")

market = st.sidebar.selectbox(
    "Select Volatility Index",
    MARKETS
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Matches & Differs"
    ]
)

st.sidebar.success(f"Market: {market}")

if page == "Dashboard":
    show_dashboard()

elif page == "Matches & Differs":
    show_matches() 
