from database import load_ticks
from matches_strategy import MatchesStrategy
from over_under_strategy import OverUnderStrategy
from learning_engine import LearningEngine
from tracker import save_signal


strategy = MatchesStrategy()

over_under_strategy = OverUnderStrategy()

learning = LearningEngine()


def get_over_under_status(market):
    """
    Runs automatically on every rerun/tick - no button needed.

    Loads enough ticks to build the full snapshot series (up to
    WINDOW + STEP * (NUM_SNAPSHOTS - 1) ticks) and returns the
    current Over/Under 5 signal, confidence, trend, and acceleration.

    This is a pure READ, same as get_live_status - it never logs
    anything on its own.
    """

    needed = (
        over_under_strategy.WINDOW
        + over_under_strategy.STEP * (over_under_strategy.NUM_SNAPSHOTS - 1)
    )

    history = load_ticks(market, limit=needed)

    result = over_under_strategy.analyze(history)

    result["ticks_available"] = len(history)
    result["ticks_needed"] = needed

    return result


def get_live_status(market):
    """
    Runs automatically on every rerun/tick - no button needed.

    Pulls the latest available ticks and recomputes everything fresh
    every single time this is called: current percentages, ranking,
    and the gaining check against the older half of the same window.
    As soon as a new tick lands, the next call sees it - there is no
    caching or stale state here.

    This is purely a READ - it never logs anything. Logging only
    happens via log_current_signal(), when SCAN is pressed.
    """

    history = load_ticks(market, limit=strategy.WINDOW)

    result = strategy.analyze(history)

    return {

        "target_digit": result["target_digit"],
        "confidence": result["confidence"],
        "duration": 1,
        "valid": result["valid"],
        "entry_active": result["entry_active"],
        "reason": result["reason"],
        "top_digit": result["top_digit"],
        "top_percent": result["top_percent"],
        "second_digit": result["second_digit"],
        "second_percent": result["second_percent"],
        "third_digit": result["third_digit"],
        "third_percent": result["third_percent"],
        "gaining": result["gaining"],
        "live_digit": result["live_digit"],
        "ranking": result["ranking"],
        "full_percentages": result["full_percentages"],
        "ticks_available": len(history),

    }


def log_current_signal(market, status, duration=1):
    """
    Called when SCAN is pressed. Logs the CURRENT status (the same
    one already shown on screen, computed fresh this render) as a
    real prediction for accuracy tracking - but only if it's an
    actual match (entry_active). A no-match result logs nothing.

    Returns True if a prediction was logged, False otherwise.
    """

    if not status.get("entry_active"):
        return False

    target = status["target_digit"]

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
        frequency_score=status.get("top_percent", 0),
        momentum_score=status.get("second_percent", 0),
        transition_score=status.get("third_percent", 0),
        confidence=status["confidence"],
        signal="MATCH",
        duration=duration

    )

    return True
