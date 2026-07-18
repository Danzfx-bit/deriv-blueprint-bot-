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
    font-weight:900;
    color:#D32F2F;
}

.bp-subtitle{
    font-size:16px;
    color:#666;
}

.bp-section{
    font-size:22px;
    font-weight:800;
    color:#D32F2F;
    margin-top:15px;
    margin-bottom:12px;
}

.bp-label{
    font-size:13px;
    color:#777;
    text-transform:uppercase;
}

.bp-value{
    font-size:34px;
    font-weight:900;
    color:#222;
}

</style>
""", unsafe_allow_html=True)



# =====================================================
# Card Function
# =====================================================

def metric_card(title,value):

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


    ticks = get_tick_count(market)


    history = load_ticks(
        market,
        limit=100
    )


    latest_digit="-"


    if len(history)>0:

        latest_digit = history[-1]



    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
    """
    <div class="bp-card">

        <div class="bp-title">
        🧠 Blueprint Intelligence
        </div>

        <div class="bp-subtitle">
        AI Powered Digit Prediction Engine
        </div>

    </div>
    """,
    unsafe_allow_html=True
    )



    # =====================================================
    # LIVE MARKET
    # =====================================================

    st.markdown(
    """
    <div class="bp-section">
    📈 LIVE MARKET
    </div>
    """,
    unsafe_allow_html=True
    )


    c1,c2,c3 = st.columns(3)


    with c1:
        metric_card(
            "Market",
            market
        )


    with c2:
        metric_card(
            "Stored Ticks",
            ticks
        )


    with c3:
        metric_card(
            "Last Digit",
            latest_digit
        )



    # =====================================================
    # AI PREDICTION
    # =====================================================


    st.markdown(
    """
    <div class="bp-section">
    🎯 AI PREDICTION
    </div>
    """,
    unsafe_allow_html=True
    )


    prediction="-"
    confidence=0
    duration="1 Tick"



    if "scan_result" in st.session_state:

        result = st.session_state["scan_result"]

        prediction=result.get(
            "target_digit",
            "-"
        )

        confidence=result.get(
            "confidence",
            0
        )

        duration=f"{result.get('duration',1)} Tick"



    st.markdown(
    f"""
    <div class="bp-card"
    style="
    text-align:center;
    border:3px solid #D32F2F;
    ">

        <div class="bp-label">
        NEXT DIGIT
        </div>


        <div style="
        font-size:90px;
        font-weight:900;
        color:#D32F2F;
        ">

        {prediction}

        </div>


        <div style="
        font-size:24px;
        font-weight:800;
        ">

        Confidence {confidence}%

        </div>


        <br>


        <div style="
        background:#ddd;
        height:15px;
        border-radius:10px;
        ">

            <div style="
            background:#D32F2F;
            height:15px;
            width:{confidence}%;
            border-radius:10px;
            ">
            </div>

        </div>


        <br>

        Duration: {duration}

    </div>
    """,
    unsafe_allow_html=True
    )



    # =====================================================
    # LEARNING ENGINE
    # =====================================================


    st.markdown(
    """
    <div class="bp-section">
    🧠 LEARNING ENGINE
    </div>
    """,
    unsafe_allow_html=True
    )


    stats = learning.db.get_learning_statistics()



    a,b,c = st.columns(3)


    with a:

        metric_card(
            "Predictions",
            stats["stored"]
        )

        metric_card(
            "Accuracy",
            f"{stats['accuracy']}%"
        )


    with b:

        metric_card(
            "Correct",
            stats["correct"]
        )

        metric_card(
            "Incorrect",
            stats["incorrect"]
        )


    with c:

        metric_card(
            "Validated",
            stats["validated"]
        )


        pending = stats["stored"] - stats["validated"]


        metric_card(
            "Pending",
            pending
        )



    # =====================================================
    # SYSTEM STATUS
    # =====================================================


    st.markdown(
    """
    <div class="bp-section">
    🚀 SYSTEM STATUS
    </div>
    """,
    unsafe_allow_html=True
    )


    x,y,z = st.columns(3)


    with x:

        st.success(
            "🟢 Deriv Connected"
        )


    with y:

        st.info(
            f"📊 {ticks} Live Ticks"
        )


    with z:


        if stats["accuracy"] >=70:

            st.success(
                "🔥 AI Improving"
            )

        elif stats["accuracy"] >=50:

            st.warning(
                "⚡ Learning"
            )

        else:

            st.error(
                "📚 Collecting Data"
            )


    st.markdown(
    """
    <div style="
    text-align:center;
    color:white;
    padding:15px;
    ">
    Blueprint Intelligence Engine © 2026
    </div>
    """,
    unsafe_allow_html=True
    )
