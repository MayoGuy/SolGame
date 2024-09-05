import random
from typing import Dict, Tuple


class Island:
    def __init__(
        self, id: str, 
        player_id: int, 
        pos: tuple[int, int], 
        value: int, 
        income:int, 
        natives: bool, 
        main: bool,
        reinforcements: Tuple[int, int] #(player_id, num_reinforcements)
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
    def __init__(self, id: int):
        self.id = id


class Game:
    def __init__(self, players: int):
        self.players = {i:Player(i, 15) for i in range(players)}
        self.islands = self.generate_islands()
        self.lost = []

    # Make the island Generation logic
    def generate_islands():
        islands: Dict[str, Island] = []
        return islands
    

    def move(self, previous_island: str, island_id: str, player_id: int, rs:int, reinforcement_id:int=None):
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
        
    



        


    