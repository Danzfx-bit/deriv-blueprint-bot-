import os
import time
import pandas as pd
from datetime import datetime

SIGNALS_FILE = "data/signals.csv"

last_signal = None
last_time = 0


def save_signal(market, signal, digit, probability, duration):

    global last_signal, last_time

    current_signal = (
        market,
        signal,
        digit
    )

    # Prevent duplicate signals within 30 seconds
    if (
        current_signal == last_signal
        and (time.time() - last_time) < 30
    ):
        return

    last_signal = current_signal
    last_time = time.time()

    os.makedirs("data", exist_ok=True)

    new_signal = pd.DataFrame([{
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "market": market,
        "signal": signal,
        "digit": digit,
        "probability": probability,
        "duration": duration,
        "status": "PENDING",
        "result": ""
    }])

    if os.path.exists(SIGNALS_FILE):

        data = pd.read_csv(SIGNALS_FILE)

        data = pd.concat(
            [data, new_signal],
            ignore_index=True
        )

    else:

        data = new_signal

    data.to_csv(
        SIGNALS_FILE,
        index=False
    )


def load_signals():

    if not os.path.exists(SIGNALS_FILE):
        return pd.DataFrame()

    return pd.read_csv(SIGNALS_FILE)


def signal_count():

    data = load_signals()

    return len(data)


def pending_signals():

    data = load_signals()

    if data.empty:
        return data

    return data[
        data["status"] == "PENDING"
    ]


def completed_signals():

    data = load_signals()

    if data.empty:
        return data

    return data[
        data["status"] == "COMPLETE"
    ]


def statistics():

    data = load_signals()

    if data.empty:

        return {
            "total": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0
        }

    wins = len(
        data[data["result"] == "WIN"]
    )

    losses = len(
        data[data["result"] == "LOSS"]
    )

    total = wins + losses

    if total == 0:
        win_rate = 0
    else:
        win_rate = round(
            (wins / total) * 100,
            2
        )

    return {
        "total": len(data),
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate
        }
