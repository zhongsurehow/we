from game_state import GameState, Zone, Player
from cards import GuaCard

def check_zone_control(game_state: GameState, zone_name: str):
    """Checks if a zone's control has changed and updates it."""
    zone_data = game_state.board.gua_zones[zone_name]

    current_markers_total = sum(zone_data["markers"].values())
    if current_markers_total < zone_data["limit"]:
        return

    if not zone_data["markers"]:
        return

    top_player_name = max(zone_data["markers"], key=zone_data["markers"].get)

    controller = next((p for p in game_state.players if p.name == top_player_name), None)

    if controller:
        print(f"--- 地利争夺: {controller.name} has gained control of {zone_name}! ---")
        zone_data["controller"] = controller
        zone_data["markers"] = {}

def play_card(game_state: GameState, card_index: int, zone_choice: str) -> bool:
    """Action for a player to play a card from their hand."""
    player = game_state.get_current_player()

    if not (0 <= card_index < len(player.hand)):
        print("Invalid card index.")
        return False

    card_to_play: GuaCard = player.hand.pop(card_index)

    if zone_choice not in card_to_play.associated_guas:
        print(f"Invalid zone choice. Must be one of {card_to_play.associated_guas}")
        player.hand.insert(card_index, card_to_play)
        return False

    print(f"{player.name} plays {card_to_play.name} and places influence in {zone_choice}.")

    player.current_task_card = card_to_play

    zone_markers = game_state.board.gua_zones[zone_choice]["markers"]
    zone_markers[player.name] = zone_markers.get(player.name, 0) + 1

    check_zone_control(game_state, zone_choice)

    return True

def move(game_state: GameState, target_zone_str: str) -> bool:
    """Action for a player to move between zones."""
    player = game_state.get_current_player()

    try:
        target_zone = Zone(target_zone_str)
    except ValueError:
        print(f"Invalid zone '{target_zone_str}'. Must be one of {[z.value for z in Zone]}.")
        return False

    # Basic validation, can be expanded with AP costs later
    current_pos = player.position
    if (current_pos == Zone.DI and target_zone == Zone.REN) or \
       (current_pos == Zone.REN and target_zone == Zone.TIAN):
        player.position = target_zone
        print(f"{player.name} moves from {current_pos.value} to {target_zone.value}.")
        game_state.board.player_positions[player.name] = player.position
        return True
    else:
        print(f"Invalid move from {current_pos.value} to {target_zone.value}.")
        return False

def complete_task(game_state: GameState, task_index: int) -> bool:
    """Action for a player to complete a task on their active card."""
    player = game_state.get_current_player()

    if not player.current_task_card:
        print("No active task card.")
        return False

    if not (0 <= task_index < 6):
        print("Invalid task index (must be 0-5).")
        return False

    task = player.current_task_card.tasks[task_index]

    player_zone_str = player.position.value

    required_zone_map = {'地': Zone.DI, '人': Zone.REN, '天': Zone.TIAN}
    required_zone = required_zone_map.get(task.level)

    if player.position != required_zone:
        print(f"Cannot complete task: Player is in {player_zone_str} but task requires {task.level}.")
        return False

    print(f"{player.name} completes task: {task.name}")

    player.dao_xing += task.reward_dao_xing
    player.cheng_yi += task.reward_cheng_yi

    print(f"  Rewards: +{task.reward_dao_xing} 道行, +{task.reward_cheng_yi} 诚意")

    # For this prototype, we just grant the base rewards.

    return True
