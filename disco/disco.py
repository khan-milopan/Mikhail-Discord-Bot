import requests
import websockets
import asyncio
import json

class Bot:
    def __init__(self, token:str):
        self.token = token
        self.req = self.req(self.token)
        self.ws = self.ws(self.token)
    
    class req:
        def __init__(self, token:str):
            self.token = token

        def send_msg(self, channel_id:str, msg_content:str):
            message = {"content":msg_content}
            requests.post(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                json=message,
                headers={"Authorization":f"Bot {self.token}", "Content-Type": "application/json"})

    class ws():
        def __init__(self, token:str):
            self.token = token
        
        def start(self):
            try:
                asyncio.run(self.connect())
            except KeyboardInterrupt:
                print("Bot stopped")

        async def connect(self) -> None:
            async with websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json") as websocket:
                hello_msg = json.loads(await websocket.recv())
                interval = hello_msg["d"]["heartbeat_interval"]

                identify = {
                    "op": 2,
                    "d": {
                        "token": self.token,
                        "intents": 513,
                        "properties": {
                        "$os": "linux",
                        "$browser": "",
                        "$device": ""
                        }
                    }
                }
                await websocket.send(json.dumps(identify))

                await self.heartbeat(websocket, interval)
        
        async def heartbeat(self,
                websocket:websockets.ClientProtocol,
                interval: int) -> None:
            
            heartbeat = {
                "op": 1,
                "d": None
            }

            while True:
                await websocket.send(json.dumps(heartbeat))
                await asyncio.sleep(interval / 1000)