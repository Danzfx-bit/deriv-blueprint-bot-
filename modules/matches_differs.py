import streamlit as st
from collections import Counter


def show():

    st.header("🎯 Matches & Differs")

    if "digit_history" not in st.session_state:
        st.info("Waiting for live tick data...")
        st.metric("Current Last Digit", "-")
        st.metric("Recommended Trade", "Waiting")
        st.metric("Confidence", "0%")
        return

    history = st.session_state["digit_history"]

    if len(history) < 1000:
        st.info(f"Collecting data... ({len(history)}/1000 ticks)")
        st.progress(len(history) / 1000)
        return

    last_digit = history[-1]

    counts = Counter(history)

    st.success("🟢 Analysis Ready")

    st.metric("Current Last Digit", last_digit)

    st.subheader("Digit Frequency")

    cols = st.columns(10)

    for digit in range(10):
        cols[digit].metric(str(digit), counts.get(digit, 0))

    most_common = counts.most_common()

    hottest_digit = most_common[0][0]
    hottest_count = most_common[0][1]

    coldest_digit = min(counts, key=counts.get)
    coldest_count = counts[coldest_digit]

    st.write("### Market Statistics")
    st.write(f"🔥 Hottest Digit: **{hottest_digit}** ({hottest_count} occurrences)")
    st.write(f"❄️ Coldest Digit: **{coldest_digit}** ({coldest_count} occurrences)")

    if last_digit == hottest_digit:
        recommendation = "DIFFER"
        confidence = 80

    elif last_digit == coldest_digit:
        recommendation = "MATCH"
        confidence = 80

    else:
        recommendation = "WAIT"
        confidence = 60

    st.metric("Recommended Trade", recommendation)
    st.metric("Confidence", f"{confidence}%")
