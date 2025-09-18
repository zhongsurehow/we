from game_state import GameState, Zone, Player
from cards import GuaCard, QIAN_WEI_TIAN # Import test card

def check_zone_control(game_state: GameState, zone_name: str):
    """Checks if a zone's control has changed and updates it."""
    zone_data = game_state.board.gua_zones[zone_name]

    # ---地利争夺 (Contention for Earthly Advantage)---
    # This logic triggers only when the number of influence markers in a zone
    # reaches its limit.
    current_markers_total = sum(zone_data["markers"].values())
    if current_markers_total < zone_data["limit"]:
        return

    # This should not happen if the total is >= limit, but as a safeguard.
    if not zone_data["markers"]:
        return

    # Find the maximum influence value in the zone.
    max_influence = 0
    for player_name, influence in zone_data["markers"].items():
        if influence > max_influence:
            max_influence = influence

    # Find all players who are tied for the maximum influence.
    tied_players_names = [
        name for name, influence in zone_data["markers"].items() if influence == max_influence
    ]

    winner_name = ""
    if len(tied_players_names) == 1:
        # No tie, clear winner.
        winner_name = tied_players_names[0]
    else:
        # It's a tie! Per the new rules, no one wins.
        print(f"--- Tie for control of {zone_name}! The zone becomes neutral. ---")
        # If there was a previous controller, they lose control.
        if zone_data["controller"] is not None:
            print(f"{zone_data['controller'].name} loses control of {zone_name}.")
            zone_data["controller"] = None
        # All markers are still cleared.
        zone_data["markers"] = {}
        return # End the function here as there is no winner.

    controller = next((p for p in game_state.players if p.name == winner_name), None)

    if controller:
        print(f"--- 地利争夺: {controller.name} has gained control of {zone_name}! ---")
        # The new controller is set.
        zone_data["controller"] = controller
        # All influence markers are removed, resetting the zone for future contention.
        zone_data["markers"] = {}

def play_card(game_state: GameState, card_index: int, zone_choice: str) -> bool:
    """Action for a player to play a card from their hand."""
    player = game_state.get_current_player()

    if not (0 <= card_index < len(player.hand)):
        print("Invalid card index.")
        return False

    card_to_play: GuaCard = player.hand.pop(card_index)

    # A card can only be played to one of its two associated Gua zones.
    if zone_choice not in card_to_play.associated_guas:
        print(f"Invalid zone choice. Must be one of {card_to_play.associated_guas}")
        # Return the card to the player's hand if the action is invalid.
        player.hand.insert(card_index, card_to_play)
        return False

    print(f"{player.name} plays {card_to_play.name} and places influence in {zone_choice}.")

    # This card now becomes the player's active set of tasks.
    player.current_task_card = card_to_play

    # Add one influence marker to the chosen zone for the current player.
    zone_markers = game_state.board.gua_zones[zone_choice]["markers"]
    zone_markers[player.name] = zone_markers.get(player.name, 0) + 1

    # After placing a marker, always check if it triggered a change in control.
    check_zone_control(game_state, zone_choice)

    return True

def move(game_state: GameState, target_zone_str: str) -> bool:
    """Action for a player to move between zones (升沉), now with Qi costs."""
    player = game_state.get_current_player()
    current_pos = player.position

    try:
        target_zone = Zone(target_zone_str)
    except ValueError:
        print(f"Invalid zone '{target_zone_str}'. Must be one of {[z.value for z in Zone]}.")
        return False

    cost = 0
    # Determine cost based on movement path
    if current_pos == Zone.DI and target_zone == Zone.REN:
        cost = 2
    elif current_pos == Zone.REN and target_zone == Zone.TIAN:
        cost = 3
    elif current_pos == Zone.TIAN and target_zone == Zone.TAIJI:
        # This is the special "太极轮回" move.
        cost = 0 # No Qi cost to enter Taiji
        player.dao_xing += 3
        player.cheng_yi += 2 # Rule update: Reward is 2 诚意
        print(f"{player.name} enters 太极轮回, gaining 3 道行 and 2 诚意!")
    else:
        print(f"Invalid move from {current_pos.value} to {target_zone.value}.")
        return False

    # Check if player has enough Qi
    if player.qi < cost:
        print(f"Not enough 阴阳之气 to move. Requires {cost}, has {player.qi}.")
        return False

    # Deduct cost and update position
    player.qi -= cost
    player.position = target_zone
    game_state.board.player_positions[player.name] = player.position
    print(f"{player.name} moves from {current_pos.value} to {target_zone.value} (cost: {cost} Qi).")

    # Note: The "return from Taiji" logic will be handled in the main game loop
    # at the start of the player's next turn.

    return True

def complete_task(game_state: GameState, task_index: int) -> bool:
    """Action for a player to complete a task (解爻) on their active card."""
    player = game_state.get_current_player()

    if not player.current_task_card:
        print("No active task card.")
        return False

    if not (0 <= task_index < 6):
        print("Invalid task index (must be 0-5).")
        return False

    task = player.current_task_card.tasks[task_index]

    # ---位与时应 (Matching Position with Opportunity)---
    # This is the core mechanic of the game. A task can only be completed
    # if the player's current zone (position) matches the task's required level.

    # Map the task's level (a string like '地') to the corresponding Zone enum.
    required_zone_map = {'地': Zone.DI, '人': Zone.REN, '天': Zone.TIAN}
    required_zone = required_zone_map.get(task.level)

    if player.position != required_zone:
        print(f"Cannot complete task: Player is in {player.position.value} but task requires {task.level}.")
        return False

    print(f"{player.name} completes task: {task.name}")

    # Grant the base rewards for completing the task.
    player.dao_xing += task.reward_dao_xing
    player.cheng_yi += task.reward_cheng_yi

    print(f"  Rewards: +{task.reward_dao_xing} 道行, +{task.reward_cheng_yi} 诚意")

    # In a full implementation, the specific *effect* of the task would be
    # triggered here. For example, drawing cards, gaining extra resources, etc.
    # This is a key area for future expansion.

    return True

def study(game_state: GameState) -> bool:
    """Action for a player to draw 2 cards (修行)."""
    player = game_state.get_current_player()

    # For the prototype, we add copies of the test card.
    # A full game would draw from a shuffled GAME_DECK.
    player.hand.append(QIAN_WEI_TIAN)
    player.hand.append(QIAN_WEI_TIAN)

    print(f"{player.name} performs 修行 and draws 2 cards.")
    return True

def meditate(game_state: GameState) -> bool:
    """Action for a player to gain 2 Qi (冥想)."""
    player = game_state.get_current_player()
    player.qi += 2
    print(f"{player.name} performs 冥想 and gains 2 阴阳之气.")
    return True
