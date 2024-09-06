from typing import List, Dict
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_id: str, player_id: int):
        await websocket.accept()
        
        if game_id not in self.active_connections:
            self.active_connections[game_id] = {}
        
        self.active_connections[game_id][player_id] = websocket
        print(f"New connection from player {player_id} in game {game_id}. Total connections: {len(self.active_connections[game_id])}")

    def disconnect(self, websocket: WebSocket, game_id: str, player_id: int):
        if game_id in self.active_connections:
            if player_id in self.active_connections[game_id]:
                del self.active_connections[game_id][player_id]
                print(f"Player {player_id} has left game {game_id}. Total connections: {len(self.active_connections[game_id])}")
                
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
                print(f"Game {game_id} has no more players connected and has been removed.")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict, game_id: str):
        if game_id in self.active_connections:
            for connection in self.active_connections[game_id].values():
                await connection.send_json(message)
