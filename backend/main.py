from fastapi import FastAPI, Depends, Query, WebSocket
from typing import Dict, Annotated
from game import Game

import random, string


app = FastAPI()
Games: Dict[str, Game] = {}


@app.get("/api/createGame")
async def create_game(players: int):
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    Games[x] = Game(players)


@app.websocket("/api/gameWs/{game_id}")
async def websocket_endpoint(*, websocket:WebSocket, game_id:str):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        # The format for sending data:
        # [{"previous_island": "island_id", "island_id": "island_id", "player_id": 0, "rs": 0} ...]
        # List of all of these moves made in the turn.
        for move in data:
            Games[game_id].move(move["previous_island"], move["island_id"], move["player_id"], move["rs"])
        send_data = {"islands": Games[game_id].encode_islands(), "lost": Games[game_id].lost}
        await websocket.send_json(send_data)