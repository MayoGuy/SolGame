from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict
from connection_manager import ConnectionManager
from game import Game

import random, string


manager = ConnectionManager()
app = FastAPI()
Games: Dict[str, Game] = {}

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def root():
    with open("index.html") as f:
        return HTMLResponse(f.read())


@app.get("/api/createGame")
async def create_game(players: int):
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    Games[x] = Game(players)
    return {"game_id": x, "message": "Game created successfully"}


@app.websocket("/api/gameWs/{game_id}")
async def websocket_endpoint(*, websocket:WebSocket, game_id:str):
    if game_id not in Games:
        await websocket.close(code=1003) 
        raise HTTPException(status_code=404, detail="Game not found")
    await websocket.accept()
    initial_message = await websocket.receive_json()
    if initial_message.get('event') == 'initialize':
        player_id = initial_message.get("data").get("player_id")
        player_name = initial_message.get("data").get("player_name")
        game = Games[game_id]
        game.add_player(player_id, player_name)
        await manager.connect(websocket, game_id, player_id)
        
        # Send the current game state to the newly connected player
        send_data = {
            "islands": game.encode_islands(),
            "lost": game.lost,
            "players": {k:game.players[k].name for k in game.players.keys()},
            "state": game.state,
            "event":"add_player_personal"
        }
        await manager.send_personal_message(send_data, websocket)
    player_list = {"players": {k:game.players[k].name for k in game.players.keys()}, "state": game.state, "event":"add_player"}
    await manager.broadcast(player_list, game_id)

    if game.is_game_ready():
        game.state = "PLAYING"
        await manager.broadcast({"message": "Game has started!", "event":"start"}, game_id)

    try: 
        while True:
            try:
                data = await websocket.receive_json()
                # The format for sending data:
                # [{"previous_island": "island_id", "island_id": "island_id", "player_id": 0, "rs": 0} ...]
                # List of all of these moves made in the turn.
                for move in data:
                    Games[game_id].move(move["previous_island"], move["island_id"], move["player_id"], move["rs"])
                send_data = {"islands": Games[game_id].encode_islands(), "lost": Games[game_id].lost, "event":"move"}
                await manager.broadcast(send_data, game_id)
            except ValueError:
                await websocket.send_json({"message": "Invalid JSON", "event":"error"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id, player_id)
        print("Client disconnected")
    except Exception as e:
        print(f"Error in game {game_id}:", e)
        await websocket.close(code=1003)
