import json
import websocket
from database import save_tick

APP_ID = "1089"
WS_URL = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"

MARKET = "R_10"      # Change when needed


def start():

    ws = websocket.create_connection(WS_URL)

    ws.send(json.dumps({
        "ticks": MARKET,
        "subscribe": 1
    }))

    print("Collector started...")

    while True:

        response = json.loads(ws.recv())

        if "tick" in response:

            quote = response["tick"]["quote"]

            digit = str(quote)[-1]

            save_tick(
                MARKET,
                quote,
                digit
            )

            print(
                quote,
                digit
            )


if __name__ == "__main__":

    start()
