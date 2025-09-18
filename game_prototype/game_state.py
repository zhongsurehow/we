from enum import Enum
from typing import Optional

# Game constants
HAND_LIMIT = 6

# Using forward declaration for type hints
class GuaCard:
    pass

class Zone(Enum):
    """Enumeration for the board zones."""
    DI = "地"
    REN = "人"
    TIAN = "天"
    TAIJI = "太极"

class Avatar:
    """Represents a player's Avatar with unique abilities."""
    def __init__(self, name: str, description: str, ability_description: str):
        self.name = name
        self.description = description
        self.ability_description = ability_description

class Player:
    """Represents a player in the game."""
    def __init__(self, name: str, avatar: Avatar):
        self.name = name
        self.avatar = avatar
        self.dao_xing: int = 0
        self.cheng_yi: int = 0
        self.qi: int = 0 # 阴阳之气 (Qi)
        self.hand: list[GuaCard] = []
        self.position: Zone = Zone.DI
        self.influence_markers: int = 15 # Example starting amount
        self.current_task_card: Optional[GuaCard] = None

class GameBoard:
    """Represents the state of the game board."""
    def __init__(self, num_players: int):
        # Per the rules, the zone limit depends on the number of players.
        if num_players == 2:
            limit = 5
        elif num_players == 3:
            limit = 6
        elif num_players >= 4:
            limit = 7
        else:
            limit = 5 # Default for safety

        # 8 Gua zones: 乾, 坤, 震, 巽, 坎, 离, 艮, 兑
        self.gua_zones = {
            "乾": {"markers": {}, "controller": None, "limit": limit},
            "坤": {"markers": {}, "controller": None, "limit": limit},
            "震": {"markers": {}, "controller": None, "limit": limit},
            "巽": {"markers": {}, "controller": None, "limit": limit},
            "坎": {"markers": {}, "controller": None, "limit": limit},
            "离": {"markers": {}, "controller": None, "limit": limit},
            "艮": {"markers": {}, "controller": None, "limit": limit},
            "兑": {"markers": {}, "controller": None, "limit": limit},
        }
        # Player positions on the board
        self.player_positions = {} # {player_name: Zone}

class GameState:
    """Represents the entire state of the game."""
    def __init__(self, players: list[Player]):
        self.board = GameBoard(num_players=len(players))
        self.players = players
        self.current_player_index = 0
        self.turn = 1
        # Initialize player positions
        for player in self.players:
            self.board.player_positions[player.name] = player.position

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def __str__(self):
        """A simple string representation of the game state."""
        player = self.get_current_player()
        output = f"--- Turn {self.turn}: Player {player.name}'s Turn ({player.avatar.name}) ---\n"
        for p in self.players:
            output += (
                f"  Player {p.name} | Pos: {p.position.value}, "
                f"气: {p.qi}, 道行: {p.dao_xing}, 诚意: {p.cheng_yi}, "
                f"Hand: {len(p.hand)} cards\n"
            )
        output += "Board State:\n"
        for zone, data in self.board.gua_zones.items():
            if data['controller']:
                output += f"  {zone} Zone: Controlled by {data['controller'].name}\n"
            else:
                markers_str = ", ".join(f"{player_name}: {count}" for player_name, count in data['markers'].items())
                if markers_str:
                    output += f"  {zone} Zone: Influence -> {markers_str}\n"
        return output
