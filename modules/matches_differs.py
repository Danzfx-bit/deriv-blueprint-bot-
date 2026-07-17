import streamlit as st
from collections import Counter


def show():

    st.header("🎯 Matches & Differs")

    if "digit_history" not in st.session_state:
        st.info("Waiting for live tick data...")
        return

    history = st.session_state["digit_history"]

    if len(history) < 1000:
    st.info(f"Collecting data... ({len(history)}/1000 ticks)")
    st.progress(len(history) / 1000)
    return

    last_digit = history[-1]

    counts = Counter(history)

    st.metric("Current Last Digit", last_digit)

    st.subheader("Digit Frequency")

    cols = st.columns(10)

    for digit in range(10):
        cols[digit].metric(str(digit), counts.get(digit, 0))

    # Simple probability engine
    least_seen = min(counts.values())
    most_seen = max(counts.values())

    if counts[last_digit] >= most_seen:
        recommendation = "DIFFER"
        confidence = 75

    elif counts[last_digit] <= least_seen:
        recommendation = "MATCH"
        confidence = 75

    else:
        recommendation = "WAIT"
        confidence = 55

    st.metric("Recommended Trade", recommendation)
    st.metric("Confidence", f"{confidence}%")
