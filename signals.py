import streamlit as st

from matches_strategy import MatchesStrategy
from learning_engine import LearningEngine
from tracker import save_signal


strategy = MatchesStrategy()

learning = LearningEngine()


def get_live_status(market):
    """
    Runs automatically on every rerun/tick - no button needed.

    Computes the current-hour vs previous-hour digit percentages,
    keeps the locked anchor/target in st.session_state (it only
    changes when a different digit takes over the #1 spot), and
    returns the current display status: target digit, confidence,
    validity, entry state, and the reason if not active yet.

    Confidence is binary by design: 98% when every condition (12%+
    threshold, top-3 gaining, live digit touching the anchor) is
    met right now, 0 otherwise - which the dashboard's existing
    "LOW CONFIDENCE" label already reflects with no extra UI logic.
    """

    snapshot = strategy.get_snapshot(market)

    anchor_key = f"matches_anchor::{market}"

    anchor_state = st.session_state.get(anchor_key)

    new_anchor, status = strategy.update_anchor(snapshot, anchor_state)

    st.session_state[anchor_key] = new_anchor

    confidence = 98 if status["entry_active"] else 0

    return {

        "target_digit": status["target_digit"],
        "confidence": confidence,
        "duration": 1,
        "valid": status["valid"],
        "entry_active": status["entry_active"],
        "reason": status["reason"],
        "top_digit": status["top_digit"],
        "second_digit": status["second_digit"],
        "ranking": snapshot.get("ranking", []),
        "full_percentages": snapshot.get("current_pct", {}),
        "live_digit": snapshot.get("live_digit", "-"),
        "snapshot": snapshot,

    }


def log_current_signal(market, status, duration=1):
    """
    Called when the SCAN button is pressed. Logs the CURRENT status
    (the same one already shown on screen) as a real prediction for
    accuracy tracking - but only when all conditions are actually
    met right now (entry_active). A null/low-confidence read isn't
    a prediction, so pressing SCAN then logs nothing.

    Returns True if a prediction was logged, False otherwise.
    """

    if not status.get("entry_active"):
        return False

    target = status["target_digit"]

    snapshot = status.get("snapshot", {})

    save_signal(

        market=market,
        signal="MATCH",
        digit=target,
        probability=status["confidence"],
        duration=duration

    )

    learning.save_prediction(

        market=market,
        predicted_digit=target,
        frequency_score=snapshot.get("top1_pct", 0),
        momentum_score=snapshot.get("top2_pct", 0),
        transition_score=snapshot.get("top3_pct", 0),
        confidence=status["confidence"],
        signal="MATCH",
        duration=duration

    )

    return True
