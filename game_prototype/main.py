import random
from game_state import GameState, Player, Avatar, Zone, HAND_LIMIT
from cards import GAME_DECK, QIAN_WEI_TIAN
import actions

# --- Avatar Definitions (from Avatars.md) ---
EMPEROR_AVATAR = Avatar(
    name="帝王",
    description="您是前朝皇室的末裔，身负着复兴王朝、再定乾坤的沉重使命。",
    ability_description="王权: 当您通过“地利争夺”成功立下一个“道标”时，您可以额外支付2点“道行”，立即在该“道標”所在的卦區，再放置一個您的“影響力標記”。"
)

HERMIT_AVATAR = Avatar(
    name="隐士",
    description="您曾是名满天下的智者，却看破了红尘纷争，选择归隐山林。",
    ability_description="逍遥游: 当您执行“升沉”移动时，所需消耗的AP永久-1（最低为1 AP）。"
)

def setup_game() -> GameState:
    """Sets up the initial game state for a 2-player game."""
    print("Setting up a new game of 《天机变·周天纪》...")
    player1 = Player(name="Alice", avatar=EMPEROR_AVATAR)
    player2 = Player(name="Bob", avatar=HERMIT_AVATAR)

    for _ in range(4):
        player1.hand.append(QIAN_WEI_TIAN)
        player2.hand.append(QIAN_WEI_TIAN)

    return GameState(players=[player1, player2])

def main_game_loop():
    """The main loop for the game CLI, now with 5-phase turns."""
    game_state = setup_game()
    turn_limit = 20

    while game_state.turn <= turn_limit:
        player = game_state.get_current_player()
        print(f"\n{'='*20} Turn {game_state.turn}: {player.name}'s Turn {'='*20}")

        # --- Pre-Turn: Handle Return from Taiji ---
        if player.position == Zone.TAIJI:
            print(f"--- {player.name} is returning from 太极轮回 (再入凡尘) ---")
            # Per the rules, player chooses a Gua zone to return to and places a free marker.
            # For the prototype, we'll pick one automatically.
            return_zone = "乾"
            player.position = Zone.DI
            game_state.board.player_positions[player.name] = Zone.DI

            # Place free influence marker
            zone_markers = game_state.board.gua_zones[return_zone]["markers"]
            zone_markers[player.name] = zone_markers.get(player.name, 0) + 1
            print(f"{player.name} returns to {Zone.DI.value}, placing a free influence marker in the {return_zone} zone.")

            # The rules also state the player must be placed on an "unoccupied starting point".
            # This level of board granularity is not in the prototype, but we acknowledge the rule here.
            print("(Rule acknowledgement: Player should be placed on an unoccupied starting point.)")


        # --- 2.1 天时阶段 (Mandate Phase) ---
        print("\n--- 2.1 天时阶段 (Mandate Phase) ---")
        print("(Skipping for prototype...)\n")

        # --- 2.2 生息阶段 (Qi Phase) ---
        print("--- 2.2 生息阶段 (Qi Phase) ---")
        for p in game_state.players:
            p.qi += 2
            print(f"{p.name} gains 2 阴阳之气. Total: {p.qi}")
        print("")

        # --- 2.3 演卦阶段 (Action Phase) ---
        print(f"--- 2.3 演卦阶段 (Action Phase): {player.name} ---")
        ap = 2
        has_completed_task_this_turn = False

        while ap > 0:
            print(f"\nYou have {ap} AP remaining.")
            print(game_state)
            print(f"--- {player.name}'s Hand ({len(player.hand)}/{HAND_LIMIT}) ---")
            for i, card in enumerate(player.hand): print(f"  [{i}] {card.name}")
            if player.current_task_card:
                print(f"--- Active Task Card: {player.current_task_card.name} ---")
                for i, task in enumerate(player.current_task_card.tasks): print(f"  [{i}] {task.name} ({task.level})")

            action_input = input(f"Action Phase (AP:{ap})> ").strip().lower().split()
            if not action_input: continue

            command = action_input[0]
            args = action_input[1:]

            try:
                if command == "play" and ap >= 2:
                    if actions.play_card(game_state, int(args[0]), args[1]): ap -= 2
                elif command == "study" and ap >= 1:
                    if actions.study(game_state): ap -= 1
                elif command == "meditate" and ap >= 1:
                    if actions.meditate(game_state): ap -= 1
                elif command == "task" and not has_completed_task_this_turn:
                    if actions.complete_task(game_state, int(args[0])): has_completed_task_this_turn = True
                elif command == "pass":
                    print(f"{player.name} ends the Action Phase.")
                    break
                else:
                    print("Invalid command or not enough AP.")
            except (ValueError, IndexError) as e:
                print(f"Invalid command arguments: {e}")

        # --- 2.4 升沉阶段 (Ascension Phase) ---
        print("\n--- 2.4 升沉阶段 (Ascension Phase) ---")
        move_input = input(f"Move? (e.g., 'move 人' or 'move 太极' or 'no')> ").strip().lower().split()
        if len(move_input) == 2 and move_input[0] == 'move':
            actions.move(game_state, move_input[1])
        else:
            print("No move performed.")


        # --- 2.5 归元阶段 (End Phase) ---
        print("\n--- 2.5 归元阶段 (End Phase) ---")
        if len(player.hand) > HAND_LIMIT:
            print(f"Hand size ({len(player.hand)}) exceeds limit ({HAND_LIMIT}).")
            discarded = player.hand.pop(0)
            print(f"Auto-discarded {discarded.name}.")
        print(f"{player.name}'s turn ends.")

        # Advance to next player
        game_state.current_player_index = (game_state.current_player_index + 1) % len(game_state.players)
        if game_state.current_player_index == 0:
            game_state.turn += 1

    print("\nGame has ended (turn limit reached).")

if __name__ == "__main__":
    main_game_loop()
