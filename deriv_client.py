import json
import time
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

    def stream_ticks(self, symbol, on_tick, stop_event, on_error=None):
        """
        Opens ONE persistent subscription to `symbol` and calls
        on_tick(quote, digit) for every tick Deriv sends, until
        stop_event is set (threading.Event).

        Runs forever (with automatic reconnect on any drop/error)
        until told to stop - meant to be run in a background
        thread, not called directly from the main Streamlit script.
        """

        while not stop_event.is_set():

            try:
                ws = websocket.create_connection(
                    self.url,
                    timeout=20
                )

                ws.send(json.dumps({
                    "ticks": symbol,
                    "subscribe": 1
                }))

                while not stop_event.is_set():

                    ws.settimeout(5)

                    try:
                        raw = ws.recv()
                    except websocket.WebSocketTimeoutException:
                        continue

                    response = json.loads(raw)

                    if "tick" in response:

                        quote = response["tick"]["quote"]
                        digit = int(str(quote)[-1])

                        on_tick(quote, digit)

                    elif "error" in response:

                        if on_error:
                            on_error(response["error"].get(
                                "message", "Unknown Deriv error"
                            ))

                        break

                ws.close()

            except Exception as e:

                if on_error:
                    on_error(str(e))

                if not stop_event.is_set():
                    time.sleep(2)
