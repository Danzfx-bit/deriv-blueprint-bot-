import threading

from deriv_client import DerivClient
import streamlit as st

from dashboard import show_dashboard
from modules.matches_differs import show as show_matches
from config import APP_NAME, MARKETS, TIMEFRAMES
from database import save_tick, get_tick_count
from learning_engine import LearningEngine
from live_tick_buffer import LiveTickBuffer, AutoTradeToggle
import auto_trader


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


if "auto_trade_toggle" not in st.session_state:
    st.session_state["auto_trade_toggle"] = AutoTradeToggle()

auto_trade_enabled = st.sidebar.checkbox(
    "🤖 Enable Auto-Trading (places real demo trades)",
    value=False,
    help=f"When on, places a ${auto_trader.STAKE:.2f} {auto_trader.CURRENCY} "
         f"trade the instant a match fires, up to {auto_trader.MAX_TRADES_PER_DAY}/day."
)

st.session_state["auto_trade_toggle"].set(auto_trade_enabled)

if auto_trade_enabled:
    st.sidebar.warning("🤖 Auto-trading is LIVE on this account.")
else:
    st.sidebar.caption("Auto-trading is off.")


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

    def _make_on_tick(target_market, buffer, toggle):

        def _on_tick(quote, digit):

            buffer.set_tick(quote, digit)

            # These open their own sqlite connections per call, so
            # they're safe to call from this background thread.
            save_tick(target_market, quote, digit)
            learning.validate_prediction(digit)

            if toggle.get():
                auto_trader.check_and_trade(
                    target_market, APP_ID, API_TOKEN
                )

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
            _make_on_tick(
                market,
                new_buffer,
                st.session_state["auto_trade_toggle"]
            ),
            new_stop_event,
            _make_on_error(new_buffer),
        ),
        daemon=True,
    )

    thread.start()


# ---------------- Live page content (fast, no full-page dim) ---------------- #
#
# Two separate fragments, each rerunning on its own fast timer. A
# fragment can only write elements into the container it's CALLED
# from - writing to st.sidebar.xxx from a fragment invoked at the
# main page level isn't allowed, so the sidebar status fragment is
# invoked from inside a `with st.sidebar:` block instead, using bare
# st.xxx() calls (which then correctly land in the sidebar).

@st.fragment(run_every=1)
def _live_sidebar_status():

    tick_info = st.session_state["tick_buffer"].get()

    if tick_info["connected"]:
        st.success(f"🟢 Live · digit {tick_info['digit']}")
    elif tick_info["error"]:
        st.error(f"🔴 {tick_info['error']}")
    else:
        st.info("🟡 Connecting to Deriv...")


@st.fragment(run_every=1)
def _live_page_content():

    if page == "Dashboard":

        show_dashboard(market)

    elif page == "Matches & Differs":

        show_matches()


with st.sidebar:
    _live_sidebar_status()

_live_page_content()
