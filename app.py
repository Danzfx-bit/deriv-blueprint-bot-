from deriv_client import DerivClient
import streamlit as st

APP_ID = st.secrets["APP_ID"]
API_TOKEN = st.secrets["API_TOKEN"]

from dashboard import show_dashboard
from modules.matches_differs import show as show_matches
from config import APP_NAME, MARKETS, TIMEFRAMES

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)

# ---------------- Sidebar ---------------- #

st.sidebar.title("NUTEC Blueprint AI")

market_name = st.sidebar.selectbox(
    "Select Volatility Index",
    list(MARKETS.keys()),
    key="market_select"
)

market = MARKETS[market_name]

timeframe_name = st.sidebar.selectbox(
    "Select Timeframe",
    list(TIMEFRAMES.keys()),
    index=1,
    key="timeframe_select"
)

timeframe = TIMEFRAMES[timeframe_name]

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Matches & Differs"
    ],
    key="navigation_radio"
)

st.sidebar.success(f"Market: {market_name}")
st.sidebar.info(f"Timeframe: {timeframe_name}")

st.divider()

# ---------------- Live Market ---------------- #

st.subheader("📈 Live Market")

try:
    client = DerivClient(APP_ID)

    data = client.get_latest_tick(market)

    st.write(data)  # Temporary for debugging

    if "tick" in data:
        quote = data["tick"]["quote"]
        last_digit = str(quote)[-1]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Current Price", quote)

        with col2:
            st.metric("Last Digit", last_digit)

        st.success("🟢 Connected to Deriv")

    else:
        st.error("No tick data received.")

except Exception as e:
    st.error(f"Connection Error: {e}")

# ---------------- Pages ---------------- #

if page == "Dashboard":
    show_dashboard()

elif page == "Matches & Differs":
    show_matches()
