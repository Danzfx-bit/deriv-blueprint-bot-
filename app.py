from deriv_client import DerivClient
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dashboard import show_dashboard
from modules.matches_differs import show as show_matches
from config import APP_NAME, MARKETS, TIMEFRAMES
from database import save_tick, load_ticks, get_tick_count


APP_ID = st.secrets["APP_ID"]
API_TOKEN = st.secrets["API_TOKEN"]


st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)


# Refresh every 10 seconds
st_autorefresh(
    interval=10000,
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
    ]
)


st.sidebar.success(
    f"Market: {market_name}"
)

st.sidebar.info(
    f"Timeframe: {timeframe_name}"
)


st.divider()


# ---------------- Load Stored Data ---------------- #

if "digit_history" not in st.session_state:

    st.session_state["digit_history"] = load_ticks(
        market,
        limit=1000
    )


# ---------------- Live Market ---------------- #

st.subheader("📈 Live Market")


try:

    client = DerivClient(APP_ID)

    data = client.get_latest_tick(
        market
    )


    if "tick" in data:

        quote = data["tick"]["quote"]

        last_digit = str(quote)[-1]


        # Save permanently
        save_tick(
            market,
            quote,
            last_digit
        )


        # Update memory
        st.session_state["digit_history"].append(
            int(last_digit)
        )


        if len(st.session_state["digit_history"]) > 1000:

            st.session_state["digit_history"].pop(0)


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


        st.success(
            "🟢 Connected to Deriv"
        )


        st.info(
            f"Stored Ticks: {get_tick_count(market)}"
        )


    else:

        st.error(
            "No tick received"
        )


except Exception as e:

    st.error(
        f"Connection Error: {e}"
    )



# ---------------- Pages ---------------- #

if page == "Dashboard":

    show_dashboard()


elif page == "Matches & Differs":

    show_matches()
