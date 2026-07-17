import streamlit as st
from signals import analyze_digits


def show():

    st.header("🎯 Matches & Differs")

    # Check if tick history exists
    if "digit_history" not in st.session_state:
        st.info("Waiting for live tick data...")

        st.metric("Current Last Digit", "-")
        st.metric("Recommended Trade", "Waiting")
        st.metric("Confidence", "0%")

        return


    history = st.session_state["digit_history"]


    # Wait for enough data
    if len(history) < 1000:
        st.info(
            f"Collecting data... ({len(history)}/1000 ticks)"
        )

        st.progress(len(history) / 1000)

        return


    # Run analysis from signals.py
    analysis = analyze_digits(history)


    st.success("🟢 Blueprint Analysis Ready")


    col1, col2 = st.columns(2)


    with col1:
        st.metric(
            "Current Last Digit",
            analysis["current_digit"]
        )

    with col2:
        st.metric(
            "Digit Frequency",
            analysis.get("frequency", "-")
        )


    st.divider()


    col3, col4 = st.columns(2)


    with col3:
        st.metric(
            "MATCH Probability",
            f'{analysis["match_probability"]}%'
        )


    with col4:
        st.metric(
            "DIFFER Probability",
            f'{analysis["differ_probability"]}%'
        )


    st.divider()


    st.metric(
        "Recommended Trade",
        analysis["recommendation"]
    )


    st.metric(
        "Confidence",
        f'{analysis["confidence"]}%'
    )


    # Recent digit display
    st.subheader("📊 Last 20 Digits")

    recent = history[-20:]

    st.write(
        " ".join(map(str, recent))
    )
