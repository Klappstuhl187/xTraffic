from aiohttp import web
import jsonpickle
import arduino
import asyncio
import db_access as db

crossings = []
clients = []

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    clients.append(ws)
    print("Client connected")

    # Sende den aktuellen Zustand der Bahnübergänge an den neu verbundenen Client
    await ws.send_str(jsonpickle.encode(crossings))
    
    # Sende die bisherigen Traffic-Daten
    db_entries = jsonpickle.encode(db.get_all_entries())
    await ws.send_str(db_entries)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            crossing_id = int(msg.data)
            crossing = next((c for c in crossings if c["crossingId"] == crossing_id), None)

            if crossing:
                new_state = not crossing['state']
                await(send_update({"crossingId": crossing_id, "state": new_state}))
                arduino.write(("Gates %s" % new_state).encode())

        elif msg.type == web.WSMsgType.ERROR:
            print(f'WebSocket connection closed with exception {ws.exception()}')

    clients.remove(ws)
    print("Client disconnected")
    return ws

async def send_update(update):
    crossing_id = update["crossingId"]
    new_state = update["state"]
    print(f"Crossing {crossing_id} state updated to {'Up' if new_state else 'Down'}.")
    crossing = next((c for c in crossings if c["crossingId"] == crossing_id), None)
    if crossing:
        crossing['state'] = not crossing['state']
    
    update_data = jsonpickle.encode(update)
    for client in clients:
        if not client.closed:
            await client.send_str(update_data)
            
async def send_countdown(update):
    crossing_id = update["crossingId"]
    time = update["time"]
    print(f"Sending countdown to ws-clients: {crossing_id} - {time}.")
    update_data = jsonpickle.encode(update)
    for client in clients:
        if not client.closed:
            await client.send_str(update_data)

async def send_traffic_data(update):
    update_data = jsonpickle.encode(update)
    for client in clients:
        if not client.closed:
            await client.send_str(update_data)

def start():
    print("starting webserver...")
    app = web.Application()
    app.add_routes([web.get('/ws', websocket_handler)])
    web.run_app(app, port=3000)
    
