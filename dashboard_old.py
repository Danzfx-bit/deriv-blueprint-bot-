import streamlit as st

from database import load_ticks, get_tick_count
from signals import analyze_digits


def show_dashboard(market):

    st.title("📊 Blueprint Tool")


    st.markdown(
        """
        ### Welcome

        Welcome to Blueprint Tool.

        This application provides:

        - 📈 Live Deriv market analysis
        - 🎯 Digit prediction
        - 📊 Historical confidence learning
        - 🤖 AI-powered probability analysis
        """
    )


    st.divider()


    ticks = get_tick_count(market)


    history = load_ticks(

        market,

        limit=1000

    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(

            "Market",

            market

        )


        st.metric(

            "Total Stored Ticks",

            ticks

        )


    with col2:

        st.metric(

            "Ticks Available",

            len(history)

        )


        if len(history) > 0:

            st.metric(

                "Latest Digit",

                history[-1]

            )

        else:

            st.metric(

                "Latest Digit",

                "-"

            )


    st.divider()


    # -----------------------------------
    # Blueprint Prediction Scanner
    # -----------------------------------

    st.subheader(
        "📡 Blueprint Prediction Scanner"
    )


    if len(history) < 50:

        st.info(

            f"Collecting data... ({len(history)}/50 ticks)"

        )


    else:


        result = analyze_digits(

            history,

            market=market,

            duration=1

        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(

                "Prediction",

                result["target_digit"]

            )


        with col2:

            st.metric(

                "Confidence",

                f"{result['confidence']}%"

            )


        with col3:

            st.metric(

                "Duration",

                "1 Tick"

            )


        st.divider()


        st.subheader(

            "🏆 Top Ranked Digits"

        )


        for digit, score in result["ranking"][:10]:

            st.write(

                f"Digit {digit} → {score}%"

            )


    st.divider()


    if len(history) > 0:

        st.success(

            "🟢 Live market data available"

        )

    else:

        st.warning(

            "🟡 Waiting for market data..."

        )
