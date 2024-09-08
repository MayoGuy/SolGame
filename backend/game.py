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
    def __init__(self, id: str, name, color):
        self.id = id
        self.name = name
        self.color = color
        self.disconnected = False


class Game:
    def __init__(self, total_players: int):
        self.total_players = total_players
        self.players: Dict[str, Player] = {} 
        self.islands = {}
        self.state = "WAITING_FOR_PLAYERS"
        self.lost = []


    def start(self):
        # main islands
        for i in range(4):
            self.islands[f"m{i}"] = Island(
                id=f"m{i}",
                player_id=None,
                pos=(random.randint(0, 8), random.randint(0, 8)),
                value=0,
                income=0,
                natives=False,
                main=True,
                reinforcements=None
            )

    # Make the island Generation logic
    def generate_islands(self):
        islands: Dict[str, Island] = {}
        # main islands generation
        for i in range(4):
            player = list[self.players.keys()][i]
            islands["island"+str(i)] = Island("island"+str(i), player, (0,0), 15, 1, False, True, None)


        
        # small islands generation
        for i in range(8):
            islands["island"+str(i)] = Island("island"+str(i), None, (0,0), 0, random.randint(1, 3), False, False, None)
        
        

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
        
    
    def add_player(self, player_id: str, player_name, player_color):
        if player_id not in self.players:
            self.players[player_id] = Player(player_id, player_name, player_color)
            print(f"Player {player_id} has joined the game.")
            
        # If enough players have joined, change the game state to PLAYING
        if len(self.players) == self.total_players:
            self.state = "PLAYING"
            print("All players have joined. The game is starting!")


    def is_game_ready(self):
        return len(self.players) == self.total_players
    

    def remove_player(self, player_id: str):
        if player_id in self.players:
            del self.players[player_id]
            print(f"Player {player_id} has left the game.")