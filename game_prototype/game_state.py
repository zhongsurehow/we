from enum import Enum, auto
from typing import Optional

from game_prototype.card_base import GuaCard

# --- Core Enums ---
# Defining these here avoids circular dependencies.
class AvatarName(Enum):
    EMPEROR = "帝王"
    HERMIT = "隐士"

class BonusType(Enum):
    EXTRA_AP = auto()
    EXTRA_QI = auto()
    DRAW_CARD = auto()
    HAND_LIMIT = auto()
    EXTRA_INFLUENCE = auto()
    FREE_STUDY = auto()
    QI_DISCOUNT = auto()
    DAO_XING_ON_TASK = auto()

class Zone(Enum):
    """Enumeration for the board zones."""
    DI = "地"
    REN = "人"
    TIAN = "天"
    TAIJI = "太极"

# --- Core Data Classes ---
class Avatar:
    """Represents a player's Avatar with unique abilities."""
    def __init__(self, name: AvatarName, description: str, ability_description: str):
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
        self.qi: int = 0
        self.hand: list[GuaCard] = []
        self.position: Zone = Zone.DI
        self.influence_markers: int = 15
        self.current_task_card: Optional[GuaCard] = None
        self.placed_influence_this_turn: bool = False

class GameBoard:
    """Represents the state of the game board."""
    def __init__(self, num_players: int):
        if num_players == 2: limit = 5
        elif num_players == 3: limit = 6
        else: limit = 7
        self.base_limit = limit
        self.gua_zones = {
            "乾": {"markers": {}, "controller": None}, "坤": {"markers": {}, "controller": None},
            "震": {"markers": {}, "controller": None}, "巽": {"markers": {}, "controller": None},
            "坎": {"markers": {}, "controller": None}, "离": {"markers": {}, "controller": None},
            "艮": {"markers": {}, "controller": None}, "兑": {"markers": {}, "controller": None},
        }
        self.player_positions = {}

class GameState:
    """Represents the entire state of the game."""
    def __init__(self, players: list[Player]):
        self.board = GameBoard(num_players=len(players))
        self.players = players
        self.current_player_index = 0
        self.turn = 1
        self.current_tian_shi = None # The active Tian Shi card for the round
        for player in self.players:
            self.board.player_positions[player.name] = player.position

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def __str__(self):
        # ... (string representation logic)
        player = self.get_current_player()
        output = f"--- Turn {self.turn}: Player {player.name}'s Turn ({player.avatar.name.value}) ---\n"
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
