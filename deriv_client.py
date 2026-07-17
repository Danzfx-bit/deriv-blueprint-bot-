import json
import websocket

class DerivClient:

    def __init__(self, app_id):
        self.url = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"

    def get_latest_tick(self, symbol):
        ws = websocket.create_connection(self.url)

        ws.send(json.dumps({
            "ticks": symbol,
            "subscribe": 1
        }))

        while True:
            response = json.loads(ws.recv())

            if "tick" in response:
                ws.close()
                return response
