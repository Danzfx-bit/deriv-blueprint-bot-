import streamlit as st

from signals import analyze_digits
from database import load_ticks
from prediction_database import PredictionDatabase
from dashboard import _h, confidence_donut


MIN_TICKS = 50


def show():

    st.markdown(
        _h("""
        <div class="bp-card">
            <div class="bp-title" style="font-size:26px;">📡 BLUEPRINT PREDICTION SCANNER</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    market = st.session_state.get(
        "market"
    )

    history = load_ticks(
        market,
        limit=1000
    )

    if len(history) < MIN_TICKS:

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-banner">📡 COLLECTING DATA... ({len(history)}/{MIN_TICKS} TICKS)</div>
            </div>
            """),
            unsafe_allow_html=True
        )

        st.progress(
            len(history) / MIN_TICKS
        )

        return

    st.markdown(
        _h(f"""
        <div class="bp-card">
            <div class="bp-banner">🟢 SCANNER READY</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-label">Available Ticks</div>
                <div class="bp-value">{len(history)}</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            _h("""
            <div class="bp-card">
                <div class="bp-label" style="margin-bottom:8px;">Ready For Next Scan</div>
                <div style="color:#666; font-size:14px; font-weight:600;">
                    Press SCAN when you want a new prediction.
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

    if st.button(
        "🔍 SCAN",
        use_container_width=True
    ):

        result = analyze_digits(
            history,
            market=market,
            duration=1
        )

        st.session_state["scan_result"] = result

    if "scan_result" not in st.session_state:

        st.markdown(
            _h("""
            <div class="bp-card">
                <div class="bp-banner">🎯 PRESS SCAN TO ANALYSE THE LATEST MARKET DATA</div>
            </div>
            """),
            unsafe_allow_html=True
        )

        return

    result = st.session_state["scan_result"]

    db = PredictionDatabase()

    stats = db.get_learning_statistics()

    # =====================================================
    # PREDICTION + CONFIDENCE
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🎯</span> PREDICTION</div>
                <div class="bp-prediction-num">{result['target_digit']}</div>
                <div style="text-align:center;">
                    <span class="bp-tag">⏱ DURATION: {result['duration']} Tick</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            _h("""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🧬</span> CONFIDENCE LEVEL</div>
            """),
            unsafe_allow_html=True
        )
        confidence_donut(result["confidence"])
        st.markdown(
            _h(f"""
                <div class="bp-banner">📊 {len(history)} TICKS ANALYSED</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    # =====================================================
    # LEARNING ENGINE
    # =====================================================

    pending = stats["stored"] - stats["validated"]

    st.markdown(
        _h(f"""
        <div class="bp-card">
            <div class="bp-card-title"><span class="accent">🧬</span> LEARNING ENGINE</div>
            <div class="bp-mini-grid">
                <div class="bp-mini-box">
                    <div class="bp-label">Predictions Stored</div>
                    <div class="bp-mini-value">{stats['stored']}</div>
                </div>
                <div class="bp-mini-box">
                    <div class="bp-label">Validated</div>
                    <div class="bp-mini-value">{stats['validated']}</div>
                </div>
                <div class="bp-mini-box">
                    <div class="bp-label">Correct</div>
                    <div class="bp-mini-value green">{stats['correct']} ✓</div>
                </div>
                <div class="bp-mini-box">
                    <div class="bp-label">Incorrect</div>
                    <div class="bp-mini-value red">{stats['incorrect']} ✕</div>
                </div>
                <div class="bp-mini-box">
                    <div class="bp-label">Accuracy</div>
                    <div class="bp-mini-value">{stats['accuracy']}%</div>
                </div>
                <div class="bp-mini-box">
                    <div class="bp-label">Pending</div>
                    <div class="bp-mini-value orange">{pending}</div>
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    # =====================================================
    # TOP RANKED DIGITS + RECENT DIGITS
    # =====================================================

    col3, col4 = st.columns(2)

    with col3:
        rows_html = ""

        for i, (digit, score) in enumerate(result["ranking"], start=1):
            rows_html += _h(f"""
            <div class="bp-rank-row">
                <div class="bp-rank-num">{i}</div>
                <div class="bp-rank-digit">{digit}</div>
                <div class="bp-rank-bar-bg">
                    <div class="bp-rank-bar-fill" style="width:{score}%;"></div>
                </div>
                <div class="bp-rank-pct">{score}%</div>
            </div>
            """) + "\n"

        if not rows_html:
            rows_html = "<div style='color:#999;font-size:13px;'>No ranking data yet</div>"

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🏆</span> TOP RANKED DIGITS</div>
                {rows_html}
                <div class="bp-banner">⭐ BASED ON AI ANALYSIS</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with col4:
        recent = history[-30:]
        chips_html = ""

        for d in recent:
            chips_html += f'<div class="bp-digit-chip">{d}</div>'

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">📊</span> RECENT DIGITS</div>
                <div class="bp-digit-grid">{chips_html}</div>
                <div class="bp-banner" style="margin-top:16px;">🕐 LAST 30 DIGITS</div>
            </div>
            """),
            unsafe_allow_html=True
        )
