import streamlit as st

from signals import analyze_digits
from database import load_ticks


def show():

    st.header("📡 NUTEC Blueprint Scanner")


    market = st.session_state.get(
        "market",
        None
    )


    history = load_ticks(
        market,
        limit=1000
    )


    if len(history) < 1000:

        st.info(
            f"Collecting data... ({len(history)}/1000 ticks)"
        )

        st.progress(
            len(history) / 1000
        )

        return


    st.success(
        "🟢 Scanner Ready"
    )


    st.metric(
        "Available Ticks",
        len(history)
    )


    st.write(
        "Press SCAN when you want a new signal."
    )


    if st.button(
        "🔍 SCAN",
        use_container_width=True
    ):


        result = analyze_digits(
            history,
            market=market,
            duration=5
        )


        st.session_state["scan_result"] = result



    if "scan_result" not in st.session_state:

        st.info(
            "No scan performed yet."
        )

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
            f"{result['duration']} ticks"
        )



    with col2:

        st.metric(
            "Blueprint Score",
            f"{result['blueprint_score']}%"
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


    st.subheader(
        "🏆 Top Ranked Digits"
    )


    for index, item in enumerate(
        result["ranking"],
        start=1
    ):

        digit, score = item

        st.write(
            f"{index}. Digit {digit} → {score}%"
        )



    st.divider()


    st.subheader(
        "📊 Recent Digits"
    )


    st.write(
        " ".join(
            map(
                str,
                history[-20:]
            )
        )
    )
