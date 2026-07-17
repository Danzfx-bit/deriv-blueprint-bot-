from deriv_client import DerivClient
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from dashboard import show_dashboard
from modules.matches_differs import show as show_matches
from config import APP_NAME, MARKETS, TIMEFRAMES
from database import save_tick, get_tick_count


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
    list(MARKETS.keys())
)

market = MARKETS[market_name]


# Pass market to scanner
st.session_state["market"] = market


timeframe_name = st.sidebar.selectbox(
    "Select Timeframe",
    list(TIMEFRAMES.keys())
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


        # Save ONLY to database
        save_tick(
            market,
            quote,
            last_digit
        )


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

    show_dashboard(market) 


elif page == "Matches & Differs":

    show_matches()
