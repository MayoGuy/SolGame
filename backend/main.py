import socketio
import uvicorn
from typing import Dict
import json
from game import Game

import random, string


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = socketio.ASGIApp(sio)
Games: Dict[str, Game] = {}


def generate_color(colors=None):
    return random.choice([i for i in ["red", "blue", "green", "yellow" ] if i not in colors]) if colors else random.choice(["red", "blue", "green", "yellow"])


@sio.event
async def create_game(sid, players: int):
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
    if x in Games:
        return await sio.emit("error", "Game already exists")
    Games[x] = Game(players)
    print("Game created", players)
    await sio.enter_room(sid, x)
    await sio.emit("create_game", {"game_id": x, "message": "Game created successfully"}, room=sid)


@sio.event
async def join_game(sid, data):
    game_id = data.get("game_id")
    plater_id = sid
    player_name = data.get("player_name")

    if game_id not in Games:
        return await sio.emit("error", "Game not found")
    if Games[game_id].state != "WAITING_FOR_PLAYERS":
        return await sio.emit("error", "Game already started")
    if len(Games[game_id].players) >= Games[game_id].total_players:
        return await sio.emit("error", "Game is full")
    if plater_id in Games[game_id].players:
        return await sio.emit("error", "You are already in the game")
    
    game = Games[game_id]
    colors = [player.color for player in game.players.values()]
    player_color = generate_color(colors)
    game.add_player(plater_id, player_name, player_color)
    print(plater_id, player_name, player_color)


    await sio.enter_room(sid, game_id)
    await sio.emit("join_game", {"game_id": game_id, "message": "Joined successfully"}, room=sid)

    if game.is_game_ready():
        game.state = "PLAYING"
        game.generate_islands()
        
        for player in game.players:
            print(player, "started game")
            islands = game.encode_islands(player)
            await sio.emit("start_game", {"state": game.state, "islands": islands}, room=player)
    await sio.emit("update_players", {"players": [(k, game.players[k].name, game.players[k].color) for k in game.players.keys()]}, room=game_id)


@sio.event
async def move(sid, data):
    data = json.loads(data)
    game_id = data.get("game_id")
    player_id = sid
    previous_island = data.get("previous_island")
    island_id = data.get("island_id")
    rs = data.get("rs")
    reinforcement_id = data.get("reinforcement_id")
    if game_id not in Games:
        return await sio.emit("error", "Game not found")
    if player_id not in Games[game_id].players:
        return await sio.emit("error", "You are not in the game")
    if Games[game_id].state != "PLAYING":
        return await sio.emit("error", "Game is not in progress")
    if Games[game_id].islands[previous_island].player_id != player_id:
        return await sio.emit("error", "You are not in this island")

    Games[game_id].move(previous_island, island_id, player_id, rs, reinforcement_id)
    
    for player in Games[game_id].players:
        await sio.emit("update_islands", {"islands": Games[game_id].encode_islands(player), "lost": Games[game_id].lost}, room=player)


@sio.event
async def disconnect(sid):
    for game_id in Games:
        if sid in Games[game_id].players:
            Games[game_id].remove_player(sid)
            await sio.emit("update_players", {"players": [(k, Games[game_id].players[k].name, Games[game_id].players[k].color) for k in Games[game_id].players.keys()]}, room=game_id)
            if Games[game_id].is_game_ready():
                Games[game_id].state = "PLAYING"
                await sio.emit("start_game", {"state": Games[game_id].state}, room=game_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
