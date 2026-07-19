import threading

from deriv_client import DerivClient
import streamlit as st

from dashboard import show_dashboard
from modules.matches_differs import show as show_matches
from config import APP_NAME, MARKETS, TIMEFRAMES
from database import save_tick, get_tick_count
from learning_engine import LearningEngine
from live_tick_buffer import LiveTickBuffer


learning = LearningEngine()


APP_ID = st.secrets["APP_ID"]
API_TOKEN = st.secrets["API_TOKEN"]


st.set_page_config(
    page_title=APP_NAME,
    page_icon="📊",
    layout="wide"
)


# ---------------- Sidebar ---------------- #

st.sidebar.title(APP_NAME)


market_name = st.sidebar.selectbox(
    "Select Volatility Index",
    list(MARKETS.keys())
)

market = MARKETS[market_name]

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


# ---------------- Persistent live tick stream ---------------- #
#
# One background thread stays connected to Deriv and pushes every
# tick straight into a thread-safe buffer + the database, as it
# happens - no polling, no reconnect-per-tick. If the selected
# market changes, the old thread is stopped and a fresh one starts
# for the new market.

if st.session_state.get("tick_thread_market") != market:

    old_stop_event = st.session_state.get("tick_stop_event")

    if old_stop_event is not None:
        old_stop_event.set()

    new_stop_event = threading.Event()
    new_buffer = LiveTickBuffer()

    st.session_state["tick_stop_event"] = new_stop_event
    st.session_state["tick_buffer"] = new_buffer
    st.session_state["tick_thread_market"] = market

    def _make_on_tick(target_market, buffer):

        def _on_tick(quote, digit):

            buffer.set_tick(quote, digit)

            # These open their own sqlite connections per call, so
            # they're safe to call from this background thread.
            save_tick(target_market, quote, digit)
            learning.validate_prediction(digit)

        return _on_tick

    def _make_on_error(buffer):

        def _on_error(message):
            buffer.set_error(message)

        return _on_error

    client = DerivClient(APP_ID)

    thread = threading.Thread(
        target=client.stream_ticks,
        args=(
            market,
            _make_on_tick(market, new_buffer),
            new_stop_event,
            _make_on_error(new_buffer),
        ),
        daemon=True,
    )

    thread.start()


# ---------------- Live page content (fast, no full-page dim) ---------------- #
#
# This fragment reruns on its own fast timer, independent of the
# rest of the script - only this region of the page updates, so
# there's no full-page "running" overlay/dim on every tick.

@st.fragment(run_every=1)
def _live_content():

    tick_info = st.session_state["tick_buffer"].get()

    if tick_info["connected"]:
        st.sidebar.success(f"🟢 Live · digit {tick_info['digit']}")
    elif tick_info["error"]:
        st.sidebar.error(f"🔴 {tick_info['error']}")
    else:
        st.sidebar.info("🟡 Connecting to Deriv...")

    if page == "Dashboard":

        show_dashboard(market)

    elif page == "Matches & Differs":

        show_matches()


_live_content()
