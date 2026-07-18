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
.stApp{
    background:#9598A1;
}
.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}
.bp-card{
    background:white;
    border-radius:18px;
    padding:20px;
    margin-bottom:20px;
    box-shadow:0 6px 15px rgba(0,0,0,.18);
}
.bp-title{
    font-size:34px;
    font-weight:800;
    color:#D32F2F;
}
.bp-subtitle{
    font-size:16px;
    color:#666666;
}
.bp-section{
    font-size:22px;
    font-weight:700;
    color:#D32F2F;
    margin-top:15px;
    margin-bottom:12px;
}
.bp-label{
    font-size:13px;
    color:#777777;
    text-transform:uppercase;
}
.bp-value{
    font-size:34px;
    font-weight:800;
    color:#222222;
}
div.stButton > button{
    width:100%;
    background:#D32F2F;
    color:white;
    border:none;
    border-radius:12px;
    padding:12px;
    font-weight:700;
}
div.stButton > button:hover{
    background:#B71C1C;
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
            <div class="bp-label">
                {title}
            </div>
            <div class="bp-value">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# Dashboard
# =====================================================

def show_dashboard(market):

    ticks = get_tick_count(
        market
    )

    history = load_ticks(
        market,
        limit=100
    )

    latest_digit = "-"

    if len(history) > 0:
        latest_digit = history[-1]

    # =====================================================
    # Header
    # =====================================================

    st.markdown("""
    <div class="bp-card">
        <div class="bp-title">
            🧠 Blueprint Intelligence
        </div>
        <div class="bp-subtitle">
            AI Powered Prediction Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # Live Market
    # =====================================================

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

    # =====================================================
    # AI Prediction
    # =====================================================

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
        confidence = f"{result.get('confidence',0)}%"
        duration = f"{result.get('duration',1)} Tick"

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

    # =====================================================
    # LEARNING ENGINE
    # ===================================================== 

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
        pending = (
            stats["stored"] -
            stats["validated"]
        )
        metric_card(
            "Pending",
            pending
        )

    # =====================================================
    # System Status
    # =====================================================

    st.markdown("""
    <div class="bp-section">
        🚀 SYSTEM STATUS
    </div>
    """, unsafe_allow_html=True)

    status1, status2, status3 = st.columns(3)

    with status1:
        st.success("🟢 Deriv Connected")

    with status2:
        st.info(f"📊 {ticks} Live Ticks")

    with status3:
        if stats["accuracy"] >= 70:
            st.success("🔥 AI Improving")
        elif stats["accuracy"] >= 50:
            st.warning("⚡ Learning")
        else:
            st.error("📚 Collecting Data")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;
                color:white;
                font-size:14px;
                padding:10px;">
        Blueprint Intelligence Engine © 2026
    </div>
    """, unsafe_allow_html=True)
