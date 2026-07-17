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

    st.success("🟢 Scanner Ready")

    st.metric(
        "Stored Ticks",
        len(history)
    )

    st.write("Scanner will only analyse when you press the button below.")

    # ---------------- Scan Button ---------------- #

    if st.button("🔍 SCAN", use_container_width=True):

        result = analyze_digits(
            history,
            market="Current Market",
            duration=5
        )

        st.session_state["scan_result"] = result

    # ---------------- Show Latest Scan ---------------- #

    if "scan_result" not in st.session_state:

        st.info("No scan performed yet. Press SCAN.")

        return

    result = st.session_state["scan_result"]

    st.divider()

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
            f"{result['duration']} Ticks"
        )

    with col2:

        st.metric(
            "Blueprint Score",
            f"{result['blueprint_score']:.2f}"
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
            f"**{position}.** Digit **{digit}** — Score **{score:.2f}**"
        )

    st.divider()

    st.subheader("📈 Latest 20 Digits")

    recent = history[-20:]

    st.write(
        " ".join(map(str, recent))
    )
