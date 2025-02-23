import requests
import websockets
import asyncio
import json

class Bot:
    def __init__(self, token:str):
        self.token = token
        self.req_json = lambda msg_content: {"content":msg_content}
        self.req_header = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}

    # Requests

    def msg_send(self,
            channel_id:int, # Channel ID of where the request is performed
            msg_content:str): # The message to be sent
        requests.post(
            f"https://discord.com/api/v10/channels/{channel_id}/messages",
            json=self.req_json(msg_content),
            headers=self.req_header)
    
    def msg_edit(self,
            channel_id:int, # Channel ID of where the request is performed
            msg_content:str, # The edit to be made
            msg_to_edit:int): # ID of the message to be edited
        requests.patch(
            f"https://discord.com/api/v10/channels/{channel_id}/messages/{msg_to_edit}",
            json=self.req_json(msg_content),
            headers=self.req_header)

    def msg_delete(self,
            channel_id:int, # Channel ID of where the request is performed
            msg_to_del:int): # ID of the message to be deleted
        requests.delete(
            f"https://discord.com/api/v10/channels/{channel_id}/messages/{msg_to_del}",
            headers=self.req_header)
    # Websocket

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