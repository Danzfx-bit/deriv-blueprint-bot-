from deriv_client import DerivClient
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dashboard import show_dashboard
from modules.matches_differs import show as show_matches
from config import APP_NAME, MARKETS, TIMEFRAMES
from database import save_tick, load_ticks

APP_ID = st.secrets["APP_ID"]
API_TOKEN = st.secrets["API_TOKEN"]

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)

# Auto refresh every second for live tick collection
st_autorefresh(
    interval=1000,
    key="tick_refresh"
)

# ---------------- Sidebar ---------------- #

st.sidebar.title(APP_NAME)

market_name = st.sidebar.selectbox(
    "Select Volatility Index",
    list(MARKETS.keys()),
    key="market_select"
)

market = MARKETS[market_name]

timeframe_name = st.sidebar.selectbox(
    "Select Timeframe",
    list(TIMEFRAMES.keys()),
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

# ---------------- Load Saved Tick History ---------------- #

if "digit_history" not in st.session_state:

    saved_ticks = load_ticks(market)

    if len(saved_ticks) > 1000:
        saved_ticks = saved_ticks[-1000:]

    st.session_state["digit_history"] = saved_ticks

# ---------------- Live Market ---------------- #

st.subheader("📈 Live Market")

try:

    client = DerivClient(APP_ID)

    data = client.get_latest_tick(market)

    if "error" in data:

        st.error(data["error"])

    elif "tick" in data:

        quote = data["tick"]["quote"]
        last_digit = str(quote)[-1]

        # Save tick in memory
        st.session_state["digit_history"].append(
            int(last_digit)
        )

        # Keep only latest 1000 ticks
        if len(st.session_state["digit_history"]) > 1000:
            st.session_state["digit_history"].pop(0)

        # Save tick to database
        save_tick(
            market=market,
            price=quote,
            digit=last_digit
        )

        st.session_state["last_digit"] = last_digit

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Current Price",
                quote
            )

        with col2:
            st.metric(
                "Last Digit",
                last_digit
            )

        st.success("🟢 Connected to Deriv")

        st.subheader("📊 Recent Digits")

        recent_digits = st.session_state["digit_history"][-20:]

        st.write(
            " ".join(map(str, recent_digits))
        )

        st.info(
            f"Ticks collected: {len(st.session_state['digit_history'])}/1000"
        )

    else:

        st.error("No tick data received.")

except Exception as e:

    st.error(f"Connection Error: {e}")

# ---------------- Pages ---------------- #

if page == "Dashboard":
    show_dashboard()

elif page == "Matches & Differs":
    show_matches()
