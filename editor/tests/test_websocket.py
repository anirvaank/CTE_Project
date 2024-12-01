import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/editor/1/"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, WebSocket!")
        response = await websocket.recv()
        print(response)

asyncio.run(test_websocket())
