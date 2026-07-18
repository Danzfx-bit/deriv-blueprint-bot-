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

st.markdown(
    """
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

        margin-bottom:25px;

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
    """,
    unsafe_allow_html=True
)


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
