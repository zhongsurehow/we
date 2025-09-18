import random
import copy
from typing import Dict, Any, Optional
from game_prototype.game_state import GameState, Zone, Player, AvatarName, BonusType, Modifiers
from game_prototype.card_base import GuaCard, YaoCiTask
from game_prototype.game_data import GAME_DECK, GENERIC_YAO_CI_POOL

def check_zone_control(gs: GameState, zone_name: str): # This function mutates state, which is an exception to the pattern for now for simplicity.
    # ... (full implementation)
    pass

def play_card(game_state: GameState, card_index: int, zone_choice: str, mods: Modifiers) -> Optional[GameState]:
    new_state = copy.deepcopy(game_state)
    player = new_state.get_current_player()
    if not (0 <= card_index < len(player.hand)): return None
    card_to_play = player.hand.pop(card_index)
    if zone_choice not in card_to_play.associated_guas: return None
    player.current_task_card = card_to_play
    influence_to_place = 1 + mods.extra_influence
    zone_markers = new_state.board.gua_zones[zone_choice]["markers"]
    zone_markers[player.name] = zone_markers.get(player.name, 0) + influence_to_place
    player.placed_influence_this_turn = True
    check_zone_control(new_state, zone_choice)
    return new_state

def move(game_state: GameState, target_zone_str: str, mods: Modifiers) -> Optional[GameState]:
    new_state = copy.deepcopy(game_state)
    player = new_state.get_current_player()
    # ... (full move logic on new_state)
    return new_state

# ... and so on for every single action function: study, meditate, empower, activate_combo, ask_heart, scry
# Each one will start with `new_state = copy.deepcopy(game_state)` and end with `return new_state` or `return None`.

def get_valid_actions(game_state: GameState, player: Player, ap: int, mods: Modifiers, **flags) -> Dict[int, Dict[str, Any]]:
    # This function does not modify state, so it does not need to be changed.
    # ... (full implementation)
    return {}
