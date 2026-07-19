import streamlit as st

from signals import get_over_under_status
from dashboard import _h, _inject_css, over_under_card


def show():

    _inject_css()

    st.markdown(
        _h("""
        <div class="bp-card">
            <div class="bp-title" style="font-size:26px;">📐 OVER/UNDER 5 SCANNER</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    market = st.session_state.get(
        "market"
    )

    # =====================================================
    # Live status - fully automatic, recomputed fresh every
    # rerun/tick, same as the Matches page.
    # =====================================================

    status = get_over_under_status(market)

    ticks_available = status.get("ticks_available", 0)
    ticks_needed = status.get("ticks_needed", 0)

    if len(status.get("snapshots", [])) < 3:

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-banner">📡 COLLECTING DATA... ({ticks_available}/{ticks_needed} TICKS)</div>
            </div>
            """),
            unsafe_allow_html=True
        )

        if ticks_needed:
            st.progress(
                min(1.0, ticks_available / ticks_needed)
            )

        return

    st.markdown(
        _h("""
        <div class="bp-card">
            <div class="bp-banner">🟢 SCANNER LIVE - UPDATING AUTOMATICALLY</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    # =====================================================
    # SIGNAL + CONFIDENCE
    # =====================================================

    over_under_card(status)

    # =====================================================
    # SNAPSHOT HISTORY
    # =====================================================

    snapshots = status.get("snapshots", [])

    rows_html = ""

    for i, over_pct in enumerate(snapshots):

        under_pct = round(100 - over_pct, 2)

        if i == 0:
            trend_text = "—"
        else:
            trend = round(snapshots[i] - snapshots[i - 1], 2)
            trend_text = f"{trend:+.2f}%"

        rows_html += _h(f"""
        <div class="bp-stat-row">
            <span>Update {i + 1} · Over {over_pct}% / Under {under_pct}%</span>
            <span class="bp-stat-val">{trend_text}</span>
        </div>
        """) + "\n"

    st.markdown(
        _h(f"""
        <div class="bp-card">
            <div class="bp-card-title"><span class="accent">📊</span> SNAPSHOT HISTORY (EVERY 20 TICKS)</div>
            {rows_html}
            <div class="bp-banner" style="margin-top:14px;">🕐 {ticks_available} TICKS ANALYSED · {len(snapshots)} SNAPSHOTS</div>
        </div>
        """),
        unsafe_allow_html=True
    )

    # =====================================================
    # TREND / ACCELERATION BREAKDOWN
    # =====================================================

    st.markdown(
        _h(f"""
        <div class="bp-card">
            <div class="bp-card-title"><span class="accent">📈</span> TREND &amp; ACCELERATION</div>
            <div class="bp-stat-row">
                <span>Over 5 trend</span>
                <span class="bp-stat-val">{status['over_trend']:+.2f}%</span>
            </div>
            <div class="bp-stat-row">
                <span>Over 5 acceleration</span>
                <span class="bp-stat-val">{status['over_acceleration']:+.2f}</span>
            </div>
            <div class="bp-stat-row">
                <span>Under 5 trend</span>
                <span class="bp-stat-val">{status['under_trend']:+.2f}%</span>
            </div>
            <div class="bp-stat-row">
                <span>Under 5 acceleration</span>
                <span class="bp-stat-val">{status['under_acceleration']:+.2f}</span>
            </div>
            <div class="bp-banner" style="margin-top:14px;">📐 NEEDS &gt; 2% TREND + POSITIVE ACCELERATION TO SIGNAL</div>
        </div>
        """),
        unsafe_allow_html=True
    )
