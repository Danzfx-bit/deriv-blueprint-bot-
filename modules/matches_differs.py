import streamlit as st
from signals import analyze_digits


def show():

    st.header("📡 NUTEC Blueprint Scanner")

    if "digit_history" not in st.session_state:

        st.warning("Waiting for live market connection...")

        return

    history = st.session_state["digit_history"]

    if len(history) < 1000:

        st.info(
            f"Collecting market data... ({len(history)}/1000 ticks)"
        )

        st.progress(len(history) / 1000)

        return

    result = analyze_digits(
        history,
        market="Current Market",
        duration=5
    )

    st.success("🟢 Scanner Ready")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Signal",
            result["signal"]
        )

        st.metric(
            "Target Digit",
            result["number"]
        )

        st.metric(
            "Duration",
            f'{result["duration"]} Ticks'
        )

    with col2:

        st.metric(
            "Blueprint Score",
            f'{result["blueprint_score"]:.2f}'
        )

        st.metric(
            "Confidence",
            result["confidence"]
        )

        st.metric(
            "Ticks Analysed",
            len(history)
        )

    st.divider()

    st.subheader("🏆 Top Ranked Digits")

    ranking = result["ranking"][:5]

    for position, (digit, score) in enumerate(ranking, start=1):

        st.write(
            f"**{position}.** Digit **{digit}** — Blueprint Score **{score:.2f}**"
        )

    st.divider()

    st.subheader("📊 Scanner Status")

    st.success("✓ 1000 historical ticks loaded")

    st.success("✓ Blueprint scoring active")

    st.success("✓ Ranking engine running")

    st.success("✓ Signal generated")

    st.divider()

    st.subheader("📈 Latest 20 Digits")

    recent = history[-20:]

    st.write(
        " ".join(map(str, recent))
    )
