import os
import pandas as pd
from datetime import datetime

SIGNALS_FILE = "data/signals.csv"


def save_signal(market, signal, digit, probability, duration):

    os.makedirs("data", exist_ok=True)

    new_signal = pd.DataFrame([{
        "timestamp": datetime.utcnow(),
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
        data = pd.concat([data, new_signal], ignore_index=True)
    else:
        data = new_signal

    data.to_csv(SIGNALS_FILE, index=False)


def load_signals():

    if not os.path.exists(SIGNALS_FILE):
        return pd.DataFrame()

    return pd.read_csv(SIGNALS_FILE)
