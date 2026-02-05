import asyncio
import websockets

async def test():
    uri = "ws://127.0.0.1:8000/ws/ecg"
    async with websockets.connect(uri) as websocket:
        await websocket.send("0.1,0.2,0.3,0.4,0.5,0.1")
        response = await websocket.recv()
        print("Response from server:", response)

asyncio.run(test())
