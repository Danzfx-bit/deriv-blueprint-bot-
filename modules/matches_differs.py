import streamlit as st

from database import load_ticks
from signals import get_live_status, log_current_signal
from learning_engine import LearningEngine
from dashboard import _h, confidence_donut, digit_track_widget, _inject_css


MIN_TICKS = 200


def show():

    _inject_css()

    st.markdown(
        _h("""
        <div class="bp-card">
            <div class="bp-title" style="font-size:26px;">📡 DIGIT MATCHES SCANNER</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    market = st.session_state.get(
        "market"
    )

    # =====================================================
    # Live status - fully automatic, recomputed fresh every
    # rerun/tick. SCAN only logs whatever this already shows
    # at the moment it's pressed.
    # =====================================================

    status = get_live_status(market)

    if status["ticks_available"] < MIN_TICKS:

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-banner">📡 COLLECTING DATA... ({status['ticks_available']}/{MIN_TICKS} TICKS)</div>
            </div>
            """),
            unsafe_allow_html=True
        )

        st.progress(
            status["ticks_available"] / MIN_TICKS
        )

        return

    st.markdown(
        _h("""
        <div class="bp-card">
            <div class="bp-banner">🟢 SCANNER LIVE - UPDATING EVERY TICK</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    st.markdown(
        _h(f"""
        <div class="bp-card">
            <div class="bp-label">Available Ticks</div>
            <div class="bp-value">{status['ticks_available']}</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    st.write(
        "The status below updates automatically as new ticks arrive. "
        "Press SCAN only when you want THIS moment logged for "
        "accuracy tracking."
    )

    if st.button(
        "🔍 SCAN",
        use_container_width=True
    ):

        logged = log_current_signal(
            market,
            status,
            duration=1
        )

        if logged:
            st.success(f"✅ MATCH {status['target_digit']} - logged for tracking.")
        else:
            st.info(f"⏳ NO MATCH - {status['reason']}")

    # =====================================================
    # PREDICTION + CONFIDENCE
    # =====================================================

    learning = LearningEngine()

    stats = learning.db.get_learning_statistics()

    calibration = learning.get_calibrated_confidence(status["confidence"])

    col1, col2 = st.columns(2)

    with col1:
        status_label = "🟢 MATCH" if status["entry_active"] else "⏳ NO MATCH"

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🎯</span> PREDICTION</div>
                <div class="bp-prediction-num">{status['target_digit']}</div>
                <div style="text-align:center;">
                    <span class="bp-tag">⏱ DURATION: {status['duration']} Tick</span>
                </div>
                <div class="bp-banner" style="margin-top:14px;">{status_label} · {status['reason']}</div>
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
        confidence_donut(calibration["value"])

        if calibration["calibrated"]:
            note = f"REAL WIN RATE · {calibration['sample_size']} PAST SIGNALS"
            icon = "✅"
        else:
            low, high = calibration["bucket"]
            note = f"UNCALIBRATED · {calibration['sample_size']}/{calibration['min_samples']} SIGNALS IN {low}-{high}% RANGE"
            icon = "⏳"

        st.markdown(
            _h(f"""
                <div class="bp-banner">{icon} {note}</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    # =====================================================
    # DIGIT TREND STRIP
    # =====================================================

    if status.get("full_percentages"):
        digit_track_widget(status)

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

        for i, (digit, score) in enumerate(status["ranking"], start=1):
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
                <div class="bp-banner">⭐ LIVE - UPDATING EVERY TICK</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with col4:
        recent = load_ticks(market, limit=30)
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
