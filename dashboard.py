import streamlit as st

from database import load_ticks, get_tick_count


def show_dashboard(market):

    st.title("📊 NUTEC Blueprint AI")


    st.markdown(
        """
        ### Welcome

        Welcome to NUTEC Blueprint AI.

        This application provides:

        - 📈 Live Deriv market analysis
        - 🎯 Matches & Differs signals
        - 📊 Digit probability analysis
        - 🤖 AI-powered trade recommendations
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
            "Ticks Available For Scanner",
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


    if len(history) > 0:

        st.success(
            "🟢 Live market data available"
        )

    else:

        st.warning(
            "🟡 Waiting for market data..."
        )
