import requests
import websocket

ws = websocket.WebSocket()
ws.connect

res = requests.get(
    "https://127.0.0.1:2999/liveclientdata/playerlist",
    verify=False
    )

print(res)
print(res.json())
