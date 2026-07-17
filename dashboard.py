import streamlit as st

def show_dashboard():
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

        Select a market from the sidebar to begin.
        """
    )

    st.info("Status: Waiting for live market connection...")
