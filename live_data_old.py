import json
import websocket


APP_ID = "1089"

WS_URL = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"


class DerivLive:

    def __init__(self):

        self.ws = websocket.create_connection(

            WS_URL

        )


    def subscribe_ticks(self, symbol):

        self.ws.send(json.dumps({

            "ticks": symbol,

            "subscribe": 1

        }))


    def get_tick(self):

        return json.loads(

            self.ws.recv()

        )


    def get_price(self, tick):

        try:

            return float(

                tick["tick"]["quote"]

            )

        except Exception:

            return None


    def get_last_digit(self, tick):

        price = self.get_price(tick)

        if price is None:

            return None


        return int(

            str(price)[-1]

        )


    def close(self):

        self.ws.close()
