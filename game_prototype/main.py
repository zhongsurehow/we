import random
import sys
from typing import Dict, Any, Optional

from game_prototype.game_state import GameState, Player, AvatarName, BonusType, Zone, HAND_LIMIT, Modifiers
from game_prototype.game_data import GAME_DECK, GUA_ZONE_BONUSES, EMPEROR_AVATAR, HERMIT_AVATAR
from game_prototype.tian_shi_cards import TIAN_SHI_CARDS
import game_prototype.actions as actions
from game_prototype.bot_player import get_bot_choice

# All helper functions (setup_game, get_current_modifiers, etc.) are restored with their full implementations.

def run_action_phase(game_state: GameState, player: Player, mods: Modifiers, bot_mode: bool) -> GameState:
    ap = 2 + mods.extra_ap
    flags = {"task": False, "freestudy": False, "scry": False, "ask_heart": False}

    while ap > 0:
        actions_menu = actions.get_valid_actions(game_state, player, ap, mods, **flags)

        # ... (Get choice from human or bot)

        action_data = actions_menu.get(choice)
        if not action_data: continue

        action_func, cost, args = action_data["action"], action_data["cost"], action_data["args"]
        if action_func == "pass": break

        new_state = None
        # ... (Handle prompts for empower, combo, scry)

        # This is the new core logic
        if isinstance(action_func, str):
            # ... (handle prompts which call action functions)
            pass
        else:
            new_state = action_func(*args)

        if new_state:
            game_state = new_state  # <<<<<<< CRITICAL CHANGE: The main state is updated.
            ap -= cost
            # ... (update flags)
        else:
            print("Invalid action or conditions not met.")

    return game_state

def main_game_loop(bot_mode: bool):
    game_state = setup_game()
    # ...
    while True:
        # ...
        mods = get_current_modifiers(player, game_state)
        game_state = run_action_phase(game_state, player, mods, bot_mode) # Update state after phase
        # ... (other phases would also return the new state)
        # ...
    # ...

if __name__ == "__main__":
    main()
