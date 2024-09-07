import random
from typing import Dict, Tuple


class Island:
    def __init__(
        self, id: str, 
        player_id: str, 
        pos: tuple[int, int], 
        value: int, 
        income:int, 
        natives: bool, 
        main: bool,
        reinforcements: Tuple[str, int] #(player_id, num_reinforcements)
    ):
        self.id = id
        self.player_id = player_id
        self.pos = pos
        self.value = value
        self.income = income
        self.natives = natives
        self.main = main
        self.reinforcements = reinforcements

class Player:
    def __init__(self, id: str, name):
        self.id = id
        self.name = name


class Game:
    def __init__(self, total_players: int):
        self.total_players = total_players
        self.players = {} 
        self.islands = self.generate_islands()
        self.state = "WAITING_FOR_PLAYERS"
        self.lost = []

    # Make the island Generation logic
    def generate_islands():
        islands: Dict[str, Island] = []
        return islands
    

    def move(self, previous_island: str, island_id: str, player_id: str, rs:int, reinforcement_id:int=None):
        self.islands[previous_island].rs -= rs
        island = self.islands[island_id]
        if island.player_id == player_id:
            island.value += rs
        elif island.natives or island.player_id:
            if reinforcement_id:
                island.reinforcements = (reinforcement_id, rs)
            elif rs <= island.value:
                island.value -= rs
            else:
                if island.main:
                    self.lost.append(island.player_id)
                island.player_id = player_id
                island.value = rs
        else:
            island.value += rs
            island.player_id = player_id
        self.islands[island_id] = island

    
    # Encoding the islands into JSON for sending it off
    def encode_islands(self):
        return [{a:getattr(island, a) for a in dir(island) if not a.startswith('__')} for island in self.islands]
        
    
    def add_player(self, player_id: str, player_name):
        if player_id not in self.players:
            self.players[player_id] = Player(player_id, player_name)
            print(f"Player {player_id} has joined the game.")
            
        # If enough players have joined, change the game state to PLAYING
        if len(self.players) == self.total_players:
            self.state = "PLAYING"
            print("All players have joined. The game is starting!")


    def is_game_ready(self):
        return len(self.players) == self.total_players