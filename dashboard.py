import streamlit as st

from database import (
    load_ticks,
    get_tick_count
)

from learning_engine import LearningEngine


learning = LearningEngine()


# =====================================================
# Dashboard Theme
# =====================================================

st.markdown("""
<style>

.bp-card{

    background:white;

    border-radius:18px;

    padding:20px;

    box-shadow:0 6px 15px rgba(0,0,0,.15);

    margin-bottom:20px;

}

.bp-title{

    font-size:34px;

    font-weight:800;

    color:#1E1E1E;

    margin-bottom:5px;

}

.bp-subtitle{

    font-size:16px;

    color:#666666;

    margin-bottom:20px;

}

.bp-section{

    font-size:20px;

    font-weight:700;

    color:#D32F2F;

    margin-bottom:15px;

}

.bp-value{

    font-size:36px;

    font-weight:800;

    color:#1E1E1E;

}

.bp-label{

    font-size:14px;

    color:#666666;

    text-transform:uppercase;

}

.bp-status{

    color:#2E7D32;

    font-weight:700;

    font-size:16px;

}

</style>
""", unsafe_allow_html=True)


# =====================================================
# Helper Card
# =====================================================

def metric_card(title, value):

    st.markdown(

        f"""

        <div class="bp-card">

            <div class="bp-label">{title}</div>

            <div class="bp-value">{value}</div>

        </div>

        """,

        unsafe_allow_html=True

    )


# =====================================================
# Dashboard
# =====================================================

def show_dashboard(market):

    ticks = get_tick_count(market)

    history = load_ticks(
        market,
        limit=100
    )

    latest_digit = "-"

    if len(history) > 0:

        latest_digit = history[-1]

    # =================================================
    # Header
    # =================================================

    st.markdown("""

    <div class="bp-card">

        <div class="bp-title">

            🧠 Blueprint Tool

        </div>

        <div class="bp-subtitle">

            AI Powered Prediction Engine

        </div>

    </div>

    """, unsafe_allow_html=True)

    # =================================================
    # Live Market
    # =================================================

    st.markdown("""

    <div class="bp-section">

        📈 LIVE MARKET

    </div>

    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        metric_card(

            "Market",

            market

        )

    with col2:

        metric_card(

            "Stored Ticks",

            ticks

        )

    with col3:

    metric_card(

        "Last Digit",

        latest_digit

    )

    # =================================================
    # AI Prediction
    # =================================================

    st.markdown("""

    <div class="bp-section">

        🎯 AI PREDICTION

    </div>

    """, unsafe_allow_html=True)

    prediction = "-"

    confidence = "0%"

    duration = "1 Tick"

    if "scan_result" in st.session_state:

        result = st.session_state["scan_result"]

        prediction = result.get(
            "target_digit",
            "-"
        )

        confidence = f"{result.get('confidence', 0)}%"

        duration = f"{result.get('duration', 1)} Tick"

    col1, col2 = st.columns(2)

    with col1:

        metric_card(
            "Prediction",
            prediction
        )

        metric_card(
            "Duration",
            duration
        )

    with col2:

        metric_card(
            "Confidence",
            confidence
        )

        metric_card(
            "Status",
            "READY"
        )

    # =================================================
    # Learning Engine
    # =================================================

    st.markdown("""

    <div class="bp-section">

        🧠 LEARNING ENGINE

    </div>

    """, unsafe_allow_html=True)

    stats = learning.db.get_learning_statistics()

    col1, col2, col3 = st.columns(3)

    with col1:

        metric_card(
            "Predictions",
            stats["stored"]
        )

        metric_card(
            "Accuracy",
            f"{stats['accuracy']}%"
        )

    with col2:

        metric_card(
            "Correct",
            stats["correct"]
        )

        metric_card(
            "Incorrect",
            stats["incorrect"]
        )

    with col3:

        metric_card(
            "Validated",
            stats["validated"]
        )

        pending = stats["stored"] - stats["validated"]

        metric_card(
            "Pending",
            pending
        )

    # =================================================
    # Dashboard Status
    # =================================================

    st.markdown("""

    <div class="bp-section">

        🚀 SYSTEM STATUS

    </div>

    """, unsafe_allow_html=True)

    if len(history) > 0:

        st.success("🟢 Blueprint Tool is running normally.")

    else:

        st.warning("🟡 Waiting for market data...")
