import streamlit as st
from collections import Counter

from database import (
    load_ticks,
    get_tick_count
)

from learning_engine import LearningEngine


learning = LearningEngine()


def _h(s):
    """
    Strip leading whitespace from every line of an HTML/CSS string.

    Streamlit's markdown renderer will treat any line that starts with
    4+ spaces as an indented code block and print it as literal text
    instead of rendering it. Since Python f-strings built inside
    indented functions naturally pick up that leading whitespace, we
    normalize every block here before it reaches st.markdown().
    """
    lines = [line.strip() for line in s.strip("\n").split("\n")]
    return "\n".join(lines)


# =====================================================
# Dashboard Theme
# =====================================================

def _inject_css():
    """
    Re-inject the theme CSS on every rerun.

    This must be called from inside show_dashboard() rather than left
    as module-level code: Streamlit reruns the whole script on every
    autorefresh, but Python only executes a module's top-level code
    once (on first import). If the <style> block were top-level, it
    would only ever render on the very first load and disappear on
    every subsequent autorefresh.
    """
    st.markdown(_h("""
<style>

.stApp{
background:#9598A1;
}

.block-container{
padding-top:1rem;
max-width:1200px;
}

/* ---------- Header ---------- */

.bp-header{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:20px;
}

.bp-title{
font-size:36px;
font-weight:900;
color:#1a1a1a;
letter-spacing:1px;
margin:0;
}

.bp-subtitle{
font-size:13px;
color:#666;
letter-spacing:2px;
font-weight:600;
margin-top:-4px;
}

.bp-badge{
display:inline-flex;
align-items:center;
gap:8px;
background:#e9e9e9;
color:#333;
font-weight:700;
font-size:13px;
padding:10px 18px;
border-radius:10px;
}

.bp-dot{
width:8px;
height:8px;
border-radius:50%;
background:#2ecc71;
display:inline-block;
}

/* ---------- Cards ---------- */

.bp-card{
background:white;
border-radius:18px;
padding:22px 24px;
margin-bottom:20px;
box-shadow:0 6px 15px rgba(0,0,0,.15);
}

.bp-card-title{
font-size:15px;
font-weight:800;
color:#222;
margin-bottom:16px;
display:flex;
align-items:center;
gap:8px;
}

.bp-card-title .accent{
color:#D32F2F;
}

.bp-label{
font-size:11px;
color:#999;
text-transform:uppercase;
letter-spacing:1px;
margin-bottom:4px;
}

.bp-value{
font-size:26px;
font-weight:900;
color:#1a1a1a;
}

/* ---------- Live market dark panel ---------- */

.bp-market{
background:#12172B;
border-radius:18px;
padding:24px 28px;
margin-bottom:20px;
color:white;
}

.bp-live-row{
display:flex;
align-items:center;
gap:8px;
color:#D32F2F;
font-weight:800;
font-size:13px;
letter-spacing:1px;
margin-bottom:18px;
}

.bp-live-dot{
width:9px;
height:9px;
border-radius:50%;
background:#D32F2F;
display:inline-block;
animation:pulse 1.4s infinite;
}

@keyframes pulse{
0%{opacity:1;}
50%{opacity:.3;}
100%{opacity:1;}
}

.bp-market-grid{
display:flex;
justify-content:space-between;
flex-wrap:wrap;
gap:20px;
}

.bp-market-label{
font-size:11px;
text-transform:uppercase;
letter-spacing:1px;
margin-bottom:6px;
color:#9aa0b5;
}

.bp-market-value{
font-size:26px;
font-weight:900;
color:white;
}

.bp-market-sub{
font-size:11px;
color:#7c8299;
margin-top:4px;
}

.bp-digit-big{
font-size:40px;
font-weight:900;
color:#D32F2F;
}

/* ---------- Prediction card ---------- */

.bp-prediction-num{
font-size:100px;
font-weight:900;
color:#D32F2F;
text-align:center;
line-height:1;
margin:10px 0 20px 0;
}

.bp-tag{
display:inline-flex;
align-items:center;
gap:6px;
background:#FDE8E8;
color:#D32F2F;
font-weight:700;
font-size:13px;
padding:8px 16px;
border-radius:10px;
}

.bp-button-red{
background:#D32F2F;
color:white;
text-align:center;
font-weight:800;
font-size:14px;
padding:14px;
border-radius:12px;
margin-top:16px;
}

.bp-banner{
background:#FDE8E8;
color:#D32F2F;
text-align:center;
font-weight:700;
font-size:13px;
padding:12px;
border-radius:12px;
margin-top:16px;
}

/* ---------- Confidence donut ---------- */

.bp-donut-wrap{
display:flex;
justify-content:center;
margin:10px 0 20px 0;
}

.bp-donut{
width:190px;
height:190px;
border-radius:50%;
display:flex;
align-items:center;
justify-content:center;
}

.bp-donut-inner{
width:150px;
height:150px;
border-radius:50%;
background:white;
display:flex;
flex-direction:column;
align-items:center;
justify-content:center;
}

.bp-donut-pct{
font-size:34px;
font-weight:900;
color:#1a1a1a;
}

.bp-donut-lbl{
font-size:12px;
font-weight:800;
color:#666;
letter-spacing:1px;
}

/* ---------- Learning engine grid ---------- */

.bp-mini-grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:14px;
margin-bottom:16px;
}

.bp-mini-box{
background:#F6F6F8;
border-radius:14px;
padding:16px;
}

.bp-mini-value{
font-size:26px;
font-weight:900;
color:#1a1a1a;
}

.bp-mini-value.green{ color:#2ecc71; }
.bp-mini-value.red{ color:#D32F2F; }
.bp-mini-value.orange{ color:#e6912c; }

/* ---------- Statistics rows ---------- */

.bp-stat-row{
display:flex;
justify-content:space-between;
align-items:center;
padding:12px 0;
border-bottom:1px solid #eee;
font-size:14px;
font-weight:600;
color:#333;
}

.bp-stat-row:last-child{
border-bottom:none;
}

.bp-stat-val{
font-weight:800;
color:#1a1a1a;
}

/* ---------- Ranked digits ---------- */

.bp-rank-row{
display:flex;
align-items:center;
gap:10px;
margin-bottom:14px;
}

.bp-rank-num{
width:22px;
font-weight:800;
color:#999;
font-size:13px;
}

.bp-rank-digit{
width:26px;
font-weight:900;
color:#1a1a1a;
font-size:15px;
}

.bp-rank-bar-bg{
flex:1;
background:#eee;
height:10px;
border-radius:6px;
overflow:hidden;
}

.bp-rank-bar-fill{
background:#D32F2F;
height:10px;
border-radius:6px;
}

.bp-rank-pct{
width:36px;
text-align:right;
font-size:13px;
font-weight:700;
color:#555;
}

/* ---------- Recent digits grid ---------- */

.bp-digit-grid{
display:grid;
grid-template-columns:repeat(10,1fr);
gap:8px;
}

.bp-digit-chip{
background:#F6F6F8;
color:#333;
font-weight:800;
font-size:14px;
text-align:center;
padding:10px 0;
border-radius:8px;
}

.bp-digit-chip.active{
background:#D32F2F;
color:white;
}

/* ---------- Footer ---------- */

.bp-footer{
background:#12172B;
color:#9aa0b5;
text-align:center;
padding:14px;
border-radius:14px;
font-size:13px;
font-weight:600;
margin-top:10px;
}
/* ---------- Native Streamlit widgets (st.success/info/warning/error/metric) ---------- */

.stAlert{
background:white !important;
border-radius:14px !important;
border:1px solid #eee !important;
box-shadow:0 6px 15px rgba(0,0,0,.12) !important;
padding:4px 8px !important;
}

.stAlert p{
color:#333 !important;
font-weight:600 !important;
}

.stAlert svg{
fill:#D32F2F !important;
color:#D32F2F !important;
}

div[data-testid="stMetric"]{
background:white;
border-radius:14px;
padding:16px 18px;
box-shadow:0 6px 15px rgba(0,0,0,.12);
}

div[data-testid="stMetricLabel"]{
color:#999 !important;
text-transform:uppercase;
font-size:11px;
letter-spacing:1px;
}

div[data-testid="stMetricValue"]{
color:#1a1a1a !important;
font-weight:900 !important;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
background:#12172B;
}

section[data-testid="stSidebar"] *{
color:#f0f0f5 !important;
}

section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]{
background:white;
border-radius:10px;
}

section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] *{
color:#1a1a1a !important;
}

section[data-testid="stSidebar"] .stRadio label{
color:#f0f0f5 !important;
}

section[data-testid="stSidebar"] .stAlert{
background:rgba(255,255,255,.08) !important;
border:1px solid rgba(255,255,255,.15) !important;
box-shadow:none !important;
}

section[data-testid="stSidebar"] .stAlert p{
color:#f0f0f5 !important;
}

section[data-testid="stSidebar"] hr{
border-color:rgba(255,255,255,.15) !important;
}

</style>
"""), unsafe_allow_html=True)


# =====================================================
# Card helpers
# =====================================================
# (see _inject_css above, called at the top of show_dashboard)

def metric_card(title, value):
    st.markdown(
        _h(f"""
        <div class="bp-card">
            <div class="bp-label">{title}</div>
            <div class="bp-value">{value}</div>
        </div>
        """),
        unsafe_allow_html=True
    )


def confidence_donut(confidence):
    """Render a CSS conic-gradient ring showing the confidence percentage."""

    angle = max(0, min(100, confidence)) * 3.6

    label = "HIGH CONFIDENCE"
    if confidence < 50:
        label = "LOW CONFIDENCE"
    elif confidence < 75:
        label = "MEDIUM CONFIDENCE"

    st.markdown(
        _h(f"""
        <div class="bp-donut-wrap">
            <div class="bp-donut" style="background:conic-gradient(#D32F2F {angle}deg, #e6e6e6 {angle}deg);">
                <div class="bp-donut-inner">
                    <div class="bp-donut-pct">{confidence}%</div>
                    <div class="bp-donut-lbl">{label}</div>
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )


# =====================================================
# Dashboard
# =====================================================

def show_dashboard(market):

    _inject_css()

    ticks = get_tick_count(market)

    history = load_ticks(
        market,
        limit=100
    )

    latest_digit = "-"

    if len(history) > 0:
        latest_digit = history[-1]

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        _h(f"""
        <div class="bp-header">
            <div>
                <div class="bp-title">BLUEPRINT TOOL</div>
                <div class="bp-subtitle">AI POWERED PREDICTION ENGINE</div>
            </div>
            <div style="display:flex; gap:12px;">
                <div class="bp-badge"><span class="bp-dot"></span> DERIV API &nbsp; LIVE</div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    refresh_col, _unused = st.columns([1, 5])
    with refresh_col:
        if st.button("🔄 Refresh"):
            st.rerun()

    # =====================================================
    # LIVE MARKET
    # =====================================================

    st.markdown(
        _h(f"""
        <div class="bp-market">
            <div class="bp-live-row"><span class="bp-live-dot"></span> LIVE MARKET</div>
            <div class="bp-market-grid">
                <div>
                    <div class="bp-market-label">Market</div>
                    <div class="bp-market-value">{market}</div>
                </div>
                <div>
                    <div class="bp-market-label">Last Digit</div>
                    <div class="bp-digit-big">{latest_digit}</div>
                </div>
                <div>
                    <div class="bp-market-label">Stored Ticks</div>
                    <div class="bp-market-value">{ticks}</div>
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    # =====================================================
    # AI PREDICTION + CONFIDENCE
    # =====================================================

    prediction = "-"
    confidence = 0
    duration = "1 Tick"

    if "scan_result" in st.session_state:
        result = st.session_state["scan_result"]
        prediction = result.get("target_digit", "-")
        confidence = result.get("confidence", 0)
        duration = f"{result.get('duration', 1)} Tick"

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🎯</span> AI PREDICTION</div>
                <div class="bp-prediction-num">{prediction}</div>
                <div style="text-align:center;">
                    <span class="bp-tag">⏱ DURATION: {duration}</span>
                </div>
                <div class="bp-button-red">📶 PREDICTION ACTIVE</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with col2:
        banner = "STRONG SIGNAL DETECTED" if confidence >= 70 else "SIGNAL BUILDING"

        st.markdown(
            _h("""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🧬</span> CONFIDENCE LEVEL</div>
            """),
            unsafe_allow_html=True
        )
        confidence_donut(confidence)
        st.markdown(
            _h(f"""
                <div class="bp-banner">✅ {banner}</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    # =====================================================
    # LEARNING ENGINE + STATISTICS
    # =====================================================

    stats = learning.db.get_learning_statistics()
    pending = stats["stored"] - stats["validated"]

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🧬</span> AI LEARNING ENGINE</div>
                <div class="bp-mini-grid">
                    <div class="bp-mini-box">
                        <div class="bp-label">Total Predictions</div>
                        <div class="bp-mini-value">{stats['stored']}</div>
                    </div>
                    <div class="bp-mini-box">
                        <div class="bp-label">Accuracy</div>
                        <div class="bp-mini-value">{stats['accuracy']}%</div>
                    </div>
                    <div class="bp-mini-box">
                        <div class="bp-label">Correct</div>
                        <div class="bp-mini-value green">{stats['correct']} ✓</div>
                    </div>
                    <div class="bp-mini-box">
                        <div class="bp-label">Incorrect</div>
                        <div class="bp-mini-value red">{stats['incorrect']} ✕</div>
                    </div>
                </div>
                <div class="bp-banner">📈 THE ENGINE IS LEARNING AND IMPROVING...</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with col4:
        volatility = "HIGH" if ticks > 500 else "MEDIUM" if ticks > 100 else "LOW"
        market_condition = "ACTIVE" if ticks > 0 else "IDLE"

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">📊</span> STATISTICS OVERVIEW</div>
                <div class="bp-stat-row"><span>📈 Accuracy</span><span class="bp-stat-val">{stats['accuracy']}%</span></div>
                <div class="bp-stat-row"><span>📊 Validated Predictions</span><span class="bp-stat-val">{stats['validated']}</span></div>
                <div class="bp-stat-row"><span>⏳ Pending Predictions</span><span class="bp-stat-val">{pending}</span></div>
                <div class="bp-stat-row"><span>🌪 Volatility Level</span><span class="bp-stat-val">{volatility}</span></div>
                <div class="bp-stat-row"><span>☀️ Market Condition</span><span class="bp-stat-val">{market_condition}</span></div>
            </div>
            """),
            unsafe_allow_html=True
        )

    # =====================================================
    # TOP RANKED DIGITS + RECENT DIGITS
    # =====================================================

    col5, col6 = st.columns(2)

    with col5:
        rows_html = ""

        if len(history) > 0:
            counts = Counter(history)
            total = sum(counts.values())
            top5 = counts.most_common(5)

            for i, (digit, count) in enumerate(top5, start=1):
                pct = round((count / total) * 100)
                rows_html += _h(f"""
                <div class="bp-rank-row">
                    <div class="bp-rank-num">{i}</div>
                    <div class="bp-rank-digit">{digit}</div>
                    <div class="bp-rank-bar-bg">
                        <div class="bp-rank-bar-fill" style="width:{pct}%;"></div>
                    </div>
                    <div class="bp-rank-pct">{pct}%</div>
                </div>
                """) + "\n"
        else:
            rows_html = "<div style='color:#999;font-size:13px;'>No data yet</div>"

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🔥</span> TOP RANKED DIGITS</div>
                {rows_html}
                <div class="bp-banner">⭐ BASED ON AI ANALYSIS</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with col6:
        recent = list(history[-29:]) if len(history) > 0 else []
        chips_html = ""

        for d in recent:
            chips_html += f'<div class="bp-digit-chip">{d}</div>'

        chips_html += f'<div class="bp-digit-chip active">{latest_digit if latest_digit != "-" else "?"}</div>'

        st.markdown(
            _h(f"""
            <div class="bp-card">
                <div class="bp-card-title"><span class="accent">🕐</span> RECENT DIGITS</div>
                <div class="bp-digit-grid">{chips_html}</div>
                <div class="bp-banner" style="margin-top:16px;">🕐 LAST 30 DIGITS</div>
            </div>
            """),
            unsafe_allow_html=True
        )

    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        _h("""
        <div class="bp-footer">
        🛡 Secure Connection &nbsp;|&nbsp; ● AI Engine Running
        </div>
        """),
        unsafe_allow_html=True
    )
