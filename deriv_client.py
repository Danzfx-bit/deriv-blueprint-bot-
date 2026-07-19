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

    def buy_digit_match(self, api_token, symbol, digit, stake, currency="USD", duration=1, duration_unit="t"):
        """
        Places a single Digit Matches contract for `digit` on `symbol`,
        using a fresh authorized connection (kept separate from any
        tick subscription so it doesn't interfere with that stream).

        Never raises - always returns a result dict, either:
          {"success": True, "contract_id": ..., "buy_price": ..., "payout": ..., "longcode": ...}
        or
          {"success": False, "error": "..."}
        """

        try:
            ws = websocket.create_connection(self.url, timeout=20)

            ws.send(json.dumps({"authorize": api_token}))
            auth_response = json.loads(ws.recv())

            if "error" in auth_response:
                ws.close()
                return {
                    "success": False,
                    "error": auth_response["error"].get("message", "Authorization failed")
                }

            ws.send(json.dumps({
                "buy": 1,
                "price": stake,
                "parameters": {
                    "amount": stake,
                    "basis": "stake",
                    "contract_type": "DIGITMATCH",
                    "currency": currency,
                    "duration": duration,
                    "duration_unit": duration_unit,
                    "symbol": symbol,
                    "barrier": str(digit),
                }
            }))

            buy_response = json.loads(ws.recv())
            ws.close()

            if "error" in buy_response:
                return {
                    "success": False,
                    "error": buy_response["error"].get("message", "Buy request failed")
                }

            contract = buy_response.get("buy", {})

            return {
                "success": True,
                "contract_id": contract.get("contract_id"),
                "buy_price": contract.get("buy_price"),
                "payout": contract.get("payout"),
                "longcode": contract.get("longcode"),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

