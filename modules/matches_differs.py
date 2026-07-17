import streamlit as st
from signals import analyze_digits


def show():

    st.header("📡 NUTEC Blueprint Scanner")

    if "digit_history" not in st.session_state:

        st.warning("No tick data available yet.")

        return

    history = st.session_state["digit_history"]

    if len(history) < 100:

        st.info(
            f"Collecting data... ({len(history)}/100 ticks)"
        )

        return

    result = analyze_digits(
        history,
        market="Current Market",
        duration=5
    )

    signal = result["signal"]
    digit = result["number"]
    confidence = result["confidence"]
    duration = result["duration"]
    match_probability = result["match_probability"]
    differ_probability = result["differ_probability"]

    st.success("🟢 Scanner Active")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Signal",
            signal
        )

        st.metric(
            "Target Digit",
            digit
        )

        st.metric(
            "Duration",
            f"{duration} ticks"
        )

    with col2:

        st.metric(
            "Match Score",
            f"{match_probability}%"
        )

        st.metric(
            "Differ Score",
            f"{differ_probability}%"
        )

        st.metric(
            "Confidence",
            confidence
        )

    st.divider()

    st.subheader("🏆 Top Ranked Digits")

    ranking = result["ranking"]

    for position, (digit, score) in enumerate(ranking, start=1):

        st.write(
            f"{position}. Digit {digit} → {score}%"
        )

    st.divider()

    st.subheader("📊 Analysis")

    st.write("✓ Historical frequency analysis")
    st.write("✓ Recent momentum analysis")
    st.write("✓ Top-ranked digit selection")
    st.write("✓ Confidence scoring")

    st.divider()

    st.subheader("📈 Tick Statistics")

    st.metric(
        "Ticks Analysed",
        len(history)
    )

    st.metric(
        "Latest Digit",
        history[-1]
    )
