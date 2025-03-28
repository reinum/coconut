import asyncio
import websockets
import json  # Import the JSON module

async def listen_to_websocket(map):
    uri = "ws://localhost:24050/websocket/v2/precise"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
    except Exception as e:
        print(f"Error: {e}")

async def wait_for_playing():
    uri = "ws://localhost:24050/websocket/v2"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            while True:
                message = await websocket.recv()
                try:
                    # Parse the JSON string into a dictionary
                    data = json.loads(message)
                    status = data["state"]  # Access the "state" key
                    print(f"State: {status}")
                    if status["number"] == 2:
                        map = data["directPath"]["beatmapFile"]
                        await listen_to_websocket(map)
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON: {message}")
                except KeyError:
                    print(f"'state' key not found in message: {message}")
    except Exception as e:
        print(f"Error: {e}")
    
    await listen_to_websocket()

if __name__ == "__main__":
    asyncio.run(wait_for_playing())