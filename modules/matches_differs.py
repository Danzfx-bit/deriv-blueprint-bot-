import streamlit as st


def show():
    st.header("🎯 Matches & Differs")

    st.info("Waiting for live tick data...")

    st.metric("Current Last Digit", "-")

    st.metric("Recommended Trade", "Waiting")

    st.metric("Confidence", "0%")
