import random
from typing import Dict, Any
from game_prototype.game_state import GameState, Player, AvatarName, BonusType, Zone, HAND_LIMIT
from game_prototype.game_data import GAME_DECK, QIAN_WEI_TIAN, GUA_ZONE_BONUSES, EMPEROR_AVATAR, HERMIT_AVATAR
from game_prototype.tian_shi_cards import TIAN_SHI_CARDS
import game_prototype.actions as actions

# ... (setup_game, get_controlled_bonuses, check_game_end remain the same)

def get_valid_actions(game_state: GameState, player: Player, ap: int, player_bonuses: list, task_completed: bool, free_study_used: bool) -> Dict[int, Dict[str, Any]]:
    """Generates a dictionary of valid, numbered actions for the current player."""
    valid_actions = {}
    action_num = 1

    # --- AP-Costing Actions ---
    if ap >= 2:
        for i, card in enumerate(player.hand):
            for zone in sorted(list(set(card.associated_guas))):
                valid_actions[action_num] = {"action": actions.play_card, "cost": 2, "args": (i, zone, player_bonuses), "desc": f"Play {card.name} in {zone}"}
                action_num += 1
    if ap >= 1:
        valid_actions[action_num] = {"action": actions.study, "cost": 1, "args": (game_state,), "desc": "Study (Draw 2 cards)"}
        action_num += 1
        valid_actions[action_num] = {"action": actions.meditate, "cost": 1, "args": (game_state,), "desc": "Meditate (Gain 2 Qi)"}
        action_num += 1
        if player.avatar.name == AvatarName.EMPEROR:
             valid_actions[action_num] = {"action": "empower_prompt", "cost": 1, "args": (), "desc": "Empower (Use 王权)"}
             action_num += 1

    # --- Free Actions ---
    if not task_completed and player.current_task_card:
        for i, task in enumerate(player.current_task_card.tasks):
            required_zone_map = {'地': Zone.DI, '人': Zone.REN, '天': Zone.TIAN}
            if player.position == required_zone_map.get(task.level):
                valid_actions[action_num] = {"action": actions.complete_task, "cost": 0, "args": (i, player_bonuses), "desc": f"Complete Task: {task.name}"}
                action_num += 1

    if BonusType.FREE_STUDY in player_bonuses and not free_study_used:
        valid_actions[action_num] = {"action": actions.study, "cost": 0, "args": (game_state,), "desc": "Free Study (巽 Bonus)"}
        action_num += 1

    valid_actions[action_num] = {"action": "pass", "cost": 0, "args": (), "desc": "Pass Action Phase"}
    return valid_actions

def main_game_loop():
    game_state = setup_game()
    # ... (loop setup)

    while True: # Main game loop
        # ... (turn setup and other phases)
        player = game_state.get_current_player()

        # --- Action Phase with Menu ---
        ap = 2 # ... +bonuses
        has_task_completed = False
        has_free_study_used = False

        while ap > 0:
            player_bonuses = get_controlled_bonuses(player, game_state)
            actions_menu = get_valid_actions(game_state, player, ap, player_bonuses, has_task_completed, has_free_study_used)

            print("\n--- Action Menu ---")
            for num, data in actions_menu.items(): print(f"[{num}] {data['desc']} ({data['cost']} AP)")

            try:
                choice = int(input(f"Choose action for {player.name} (AP:{ap})> "))
                action_data = actions_menu.get(choice)
                if not action_data: continue

                action_func = action_data["action"]
                cost = action_data["cost"]
                args = action_data["args"]

                if action_func == "pass": ap = 0
                elif action_func == "empower_prompt":
                    zone = input("Which zone to empower?> ")
                    if actions.empower(game_state, zone, player_bonuses): ap -= cost
                else:
                    # Prepend game_state to args for action functions
                    full_args = (game_state,) + args if not isinstance(args, tuple) or args[0] != game_state else args
                    if action_func(*full_args):
                        ap -= cost
                        if action_func == actions.complete_task: has_task_completed = True
                        if action_data.get("desc") == "Free Study (巽 Bonus)": has_free_study_used = True
            except (ValueError, KeyError):
                print("Invalid input.")

        # ... (rest of the loop)
    print("\n--- The Game Has Ended ---")

if __name__ == "__main__":
    main_game_loop()
