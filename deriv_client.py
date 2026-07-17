import json
import websocket


class DerivClient:

    def __init__(self, app_id):
        self.url = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"

    def get_latest_tick(self, symbol):

        try:
            ws = websocket.create_connection(
                self.url,
                timeout=20
            )

            ws.send(json.dumps({
                "ticks": symbol
            }))

            while True:
                response = json.loads(ws.recv())

                if "tick" in response:
                    ws.close()
                    return response

                if "error" in response:
                    ws.close()
                    return response

        except websocket.WebSocketTimeoutException:
            return {
                "error": "Deriv connection timed out"
            }

        except Exception as e:
            return {
                "error": str(e)
            }
