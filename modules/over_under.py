import streamlit as st

from signals import get_over_under_status
from dashboard import _h, _inject_css


def over_under_card(ou_status):
    """
    Renders the Over/Under 5 predictor card: current signal, graded
    confidence, Over%/Under% split, and the trend + acceleration
    numbers driving the signal.

    Lives entirely in this module - the Over/Under strategy has no
    footprint anywhere else in the app (dashboard.py only supplies
    the shared _h/_inject_css styling helpers, nothing strategy
    specific).
    """

    signal = ou_status.get("signal", "-")
    confidence = ou_status.get("confidence", 0)
    reason = ou_status.get("reason", "")
    over_pct = ou_status.get("over_percent", 0)
    under_pct = ou_status.get("under_percent", 0)
    over_trend = ou_status.get("over_trend", 0)
    under_trend = ou_status.get("under_trend", 0)
    over_accel = ou_status.get("over_acceleration", 0)
    under_accel = ou_status.get("under_acceleration", 0)

    signal_color = "#2ecc71" if signal == "OVER 5" else "#D32F2F" if signal == "UNDER 5" else "#999"

    st.markdown(
        _h(f"""
        <div class="bp-card">
            <div class="bp-card-title"><span class="accent">📐</span> OVER / UNDER 5 PREDICTOR</div>

            <div style="text-align:center;">
                <div style="font-size:44px; font-weight:900; color:{signal_color};">{signal}</div>
                <div class="bp-tag" style="margin-top:8px;">CONFIDENCE {confidence}%</div>
            </div>

            <div style="display:flex; gap:14px; margin-top:18px;">
                <div style="flex:1; background:#F6F6F8; border-radius:12px; padding:14px; text-align:center;">
                    <div class="bp-label">Over 5 (5-9)</div>
                    <div class="bp-value" style="font-size:22px;">{over_pct}%</div>
                    <div style="font-size:12px; color:#666; font-weight:700; margin-top:4px;">
                        trend {over_trend:+.2f}% · accel {over_accel:+.2f}
                    </div>
                </div>
                <div style="flex:1; background:#F6F6F8; border-radius:12px; padding:14px; text-align:center;">
                    <div class="bp-label">Under 5 (0-4)</div>
                    <div class="bp-value" style="font-size:22px;">{under_pct}%</div>
                    <div style="font-size:12px; color:#666; font-weight:700; margin-top:4px;">
                        trend {under_trend:+.2f}% · accel {under_accel:+.2f}
                    </div>
                </div>
            </div>

            <div class="bp-banner" style="margin-top:16px;">{'✅' if signal != '-' else '⏳'} {reason}</div>
        </div>
        """),
        unsafe_allow_html=True
    )


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
    # rerun/tick, same as the Matches page. No auto-trading is
    # wired to this strategy - display only.
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
