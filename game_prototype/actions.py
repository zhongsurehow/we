from game_prototype.game_state import GameState, Zone, Player, AvatarName, BonusType
from game_prototype.card_base import GuaCard
from game_prototype.game_data import QIAN_WEI_TIAN

def get_zone_limit(game_state: GameState, zone_name: str) -> int:
    """Calculates the current influence limit for a zone, including bonuses."""
    base_limit = game_state.board.base_limit
    zone_data = game_state.board.gua_zones[zone_name]
    controller = zone_data.get("controller")
    if controller and controller.avatar.name == AvatarName.EMPEROR and zone_name in ["乾", "坤"]:
        return base_limit + 1
    return base_limit

def check_zone_control(game_state: GameState, zone_name: str):
    """Checks if a zone has reached its influence limit and resolves control."""
    zone_data = game_state.board.gua_zones[zone_name]
    current_limit = get_zone_limit(game_state, zone_name)
    current_markers_total = sum(zone_data["markers"].values())
    if current_markers_total < current_limit:
        return
    if not zone_data["markers"]:
        return
    max_influence = max(zone_data["markers"].values())
    tied_players_names = [n for n, i in zone_data["markers"].items() if i == max_influence]
    if len(tied_players_names) == 1:
        winner_name = tied_players_names[0]
        controller = next((p for p in game_state.players if p.name == winner_name), None)
        if controller:
            print(f"--- 地利争夺: {controller.name} has gained control of {zone_name}! ---")
            zone_data["controller"] = controller
            zone_data["markers"] = {}
    else:
        print(f"--- Tie for control of {zone_name}! The zone becomes neutral. ---")
        # On a tie, the zone always becomes neutral, regardless of prior state.
        zone_data["controller"] = None
        zone_data["markers"] = {}

def play_card(game_state: GameState, card_index: int, zone_choice: str, player_bonuses: list) -> bool:
    """Allows the current player to play a card from their hand (演卦)."""
    player = game_state.get_current_player()
    if not (0 <= card_index < len(player.hand)): return False
    card_to_play = player.hand.pop(card_index)
    if zone_choice not in card_to_play.associated_guas:
        player.hand.insert(card_index, card_to_play)
        return False
    player.current_task_card = card_to_play
    influence_to_place = 1
    if BonusType.EXTRA_INFLUENCE in player_bonuses:
        influence_to_place += 1
        print(f"{player.name} benefits from 【震】宫, placing an extra influence!")
    zone_markers = game_state.board.gua_zones[zone_choice]["markers"]
    zone_markers[player.name] = zone_markers.get(player.name, 0) + influence_to_place
    player.placed_influence_this_turn = True
    check_zone_control(game_state, zone_choice)
    print(f"{player.name} plays {card_to_play.name}, placing {influence_to_place} influence in {zone_choice}.")
    return True

def move(game_state: GameState, target_zone_str: str, player_bonuses: list) -> bool:
    """Allows the player to move between zones (升沉), spending Qi."""
    player = game_state.get_current_player()
    current_pos = player.position
    try:
        target_zone = Zone(target_zone_str)
    except ValueError:
        return False
    cost = 0
    if current_pos == Zone.DI and target_zone == Zone.REN: cost = 2
    elif current_pos == Zone.REN and target_zone == Zone.TIAN: cost = 3
    elif current_pos == Zone.TIAN and target_zone == Zone.TAIJI:
        cost = 0
        player.dao_xing += 3
        player.cheng_yi += 2
        print(f"{player.name} enters 太极轮回, gaining 3 道行 and 2 诚意!")
    else:
        return False
    if player.avatar.name == AvatarName.HERMIT: cost = max(0, cost - 1)
    if BonusType.QI_DISCOUNT in player_bonuses: cost = max(0, cost - 1)
    if player.qi < cost:
        print(f"Not enough 阴阳之气 to move. Requires {cost}, has {player.qi}.")
        return False
    player.qi -= cost
    player.position = target_zone
    game_state.board.player_positions[player.name] = player.position
    print(f"{player.name} moves from {current_pos.value} to {target_zone.value} (cost: {cost} Qi).")
    return True

def complete_task(game_state: GameState, task_index: int, player_bonuses: list) -> bool:
    """Allows a player to complete a task (解爻) from their active card."""
    player = game_state.get_current_player()
    if not player.current_task_card or not (0 <= task_index < 6): return False
    task = player.current_task_card.tasks[task_index]
    required_zone_map = {'地': Zone.DI, '人': Zone.REN, '天': Zone.TIAN}
    if player.position != required_zone_map.get(task.level): return False
    player.dao_xing += task.reward_dao_xing
    player.cheng_yi += task.reward_cheng_yi
    if BonusType.DAO_XING_ON_TASK in player_bonuses:
        player.dao_xing += 1
        print(f"{player.name} benefits from 【兑】宫, gaining an extra 1 道行!")
    print(f"{player.name} completes task: {task.name}, gaining rewards.")
    return True

def study(game_state: GameState) -> bool:
    """Allows a player to draw cards (修行)."""
    player = game_state.get_current_player()
    cards_to_draw = 2
    tian_shi = game_state.current_tian_shi
    if tian_shi and tian_shi['effect_type'] == 'MODIFY_ACTION_EFFECT' and tian_shi['action'] == 'study':
        cards_to_draw = tian_shi['value']
        print(f"天时【{tian_shi['name']}】 is in effect!")
    for _ in range(cards_to_draw):
        player.hand.append(QIAN_WEI_TIAN)
    print(f"{player.name} performs 修行 and draws {cards_to_draw} cards.")
    return True

def meditate(game_state: GameState) -> bool:
    """Allows a player to gain 2 Qi (冥想)."""
    player = game_state.get_current_player()
    player.qi += 2
    print(f"{player.name} performs 冥想 and gains 2 阴阳之气.")
    return True

def empower(game_state: GameState, zone_name: str, player_bonuses: list) -> bool:
    """Emperor's special action to add influence, spending Qi."""
    player = game_state.get_current_player()
    if player.avatar.name != AvatarName.EMPEROR: return False
    cost = 3
    if BonusType.QI_DISCOUNT in player_bonuses: cost = max(0, cost - 1)
    tian_shi = game_state.current_tian_shi
    if tian_shi and tian_shi['effect_type'] == 'MODIFY_ACTION_COST' and tian_shi['action'] == 'empower':
        cost += tian_shi['cost_change']
        print(f"天时【{tian_shi['name']}】 is in effect!")
    if player.qi < cost:
        print(f"Not enough 阴阳之气 for 王权. Requires {cost}, has {player.qi}.")
        return False
    zone_data = game_state.board.gua_zones.get(zone_name)
    if not zone_data or player.name not in zone_data["markers"]:
        return False
    player.qi -= cost
    zone_data["markers"][player.name] += 1
    player.placed_influence_this_turn = True
    print(f"{player.name} uses 王权 in {zone_name}, spending {cost} Qi to add 1 influence.")
    check_zone_control(game_state, zone_name)
    return True

def activate_combo(game_state: GameState, combo_name: str, target_player_name: str = None) -> bool:
    """Allows a player to activate a Hexagram Combination bonus."""
    player = game_state.get_current_player()
    controlled_zones = [z for z, d in game_state.board.gua_zones.items() if d.get("controller") == player]

    if combo_name == "山泽通气":
        if "艮" in controlled_zones and "兑" in controlled_zones:
            target_player = next((p for p in game_state.players if p.name == target_player_name), None)
            if not target_player or target_player == player:
                print("Invalid target player for 山泽通气.")
                return False

            player.dao_xing += 3
            player.cheng_yi += 1
            target_player.dao_xing += 3
            target_player.cheng_yi += 1
            print(f"{player.name} activates 山泽通气 with {target_player.name}! You both gain 3 道行 and 1 诚意.")
            # In a real game, this might be a one-time use. For now, it's repeatable.
            return True

    print(f"Cannot activate combo: {combo_name}. Conditions not met.")
    return False

def ask_heart(game_state: GameState) -> bool:
    """Allows a player to spend 1 Sincerity to redraw their hand (问心)."""
    player = game_state.get_current_player()

    if player.cheng_yi < 1:
        print("Not enough 诚意 to perform 问心.")
        return False

    player.cheng_yi -= 1
    hand_size = len(player.hand)
    player.hand.clear()

    # Draw new cards
    for _ in range(hand_size):
        player.hand.append(QIAN_WEI_TIAN) # Draw test cards

    print(f"{player.name} spends 1 诚意 to perform 问心, redrawing {hand_size} cards.")
    return True
