import os
import pandas as pd
from datetime import datetime


DB_FOLDER = "data"
DB_FILE = "data/ticks.csv"


def save_tick(market, price, digit):

    os.makedirs(DB_FOLDER, exist_ok=True)

    new_data = pd.DataFrame([{
        "timestamp": datetime.utcnow(),
        "market": market,
        "price": price,
        "digit": int(digit)
    }])


    if os.path.exists(DB_FILE):

        old_data = pd.read_csv(DB_FILE)

        data = pd.concat(
            [old_data, new_data],
            ignore_index=True
        )

    else:

        data = new_data


    data.to_csv(
        DB_FILE,
        index=False
    )


def load_ticks(market=None):

    if not os.path.exists(DB_FILE):
        return []


    data = pd.read_csv(DB_FILE)


    if market:

        data = data[
            data["market"] == market
        ]


    return data["digit"].astype(int).tolist()
