from signals import get_live_status, log_current_signal
from deriv_client import DerivClient
import trade_log


# Stake per trade, in the currency below. Change this to adjust.
STAKE = 1.0
CURRENCY = "USD"

# Safety cap: stops auto-firing after this many successful trades
# in a single UTC day, regardless of how many matches keep firing.
MAX_TRADES_PER_DAY = 50


def check_and_trade(market, app_id, api_token):
    """
    Called on every incoming tick from the background stream thread.

    Checks the live strategy status right now and, if it's an actual
    match (all conditions met, including the live digit touching the
    anchor), places the trade immediately via Deriv's API - unless
    the daily trade cap has already been reached.

    Always logs what happened: the trade attempt itself (win/loss,
    success/error) goes to trade_log regardless of outcome, and a
    successful match also gets logged via log_current_signal so it
    feeds the existing accuracy-tracking/calibration system.

    Returns None if there was nothing to act on (no match, or
    disabled elsewhere), or a result/status dict otherwise.
    """

    status = get_live_status(market)

    if not status.get("entry_active"):
        return None

    if trade_log.get_todays_trade_count() >= MAX_TRADES_PER_DAY:
        return {
            "skipped": True,
            "reason": f"Daily cap of {MAX_TRADES_PER_DAY} trades reached"
        }

    client = DerivClient(app_id)

    result = client.buy_digit_match(
        api_token=api_token,
        symbol=market,
        digit=status["target_digit"],
        stake=STAKE,
        currency=CURRENCY,
    )

    trade_log.save_trade(
        market,
        status["target_digit"],
        STAKE,
        result
    )

    log_current_signal(market, status, duration=1)

    return result
