import streamlit as st


def show():

    st.header("🎯 Matches & Differs")

    if "last_digit" not in st.session_state:
        st.info("Waiting for live tick data...")

        st.metric("Current Last Digit", "-")
        st.metric("Recommended Trade", "Waiting")
        st.metric("Confidence", "0%")
        return

    last_digit = st.session_state["last_digit"]

    st.success("🟢 Live tick received")

    st.metric("Current Last Digit", last_digit)

    if last_digit in [0, 2, 4, 6, 8]:
        recommendation = "DIFFER"

    else:
        recommendation = "MATCH"

    confidence = "60%"

    st.metric("Recommended Trade", recommendation)
    st.metric("Confidence", confidence) 
