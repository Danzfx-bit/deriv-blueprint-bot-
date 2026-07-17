import websocket
import json

DERIV_WS = "wss://ws.derivws.com/websockets/v3?app_id=1089"

def get_tick(symbol):
    ws = websocket.create_connection(DERIV_WS)

    ws.send(json.dumps({
        "ticks": symbol,
        "subscribe": 1
    }))

    data = json.loads(ws.recv())

    ws.close()

    return data
