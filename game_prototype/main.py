import random
from game_state import GameState, Player, Avatar, Zone
from cards import GAME_DECK, QIAN_WEI_TIAN
import actions

# --- Avatar Definitions (from Avatars.md) ---
EMPEROR_AVATAR = Avatar(
    name="帝王",
    description="您是前朝皇室的末裔，身负着复兴王朝、再定乾坤的沉重使命。",
    ability_description="王权: 当您通过“地利争夺”成功立下一个“道标”时，您可以额外支付2点“道行”，立即在该“道标”所在的卦区，再放置一个您的“影响力标记”。"
)

HERMIT_AVATAR = Avatar(
    name="隐士",
    description="您曾是名满天下的智者，却看破了红尘纷争，选择归隐山林。",
    ability_description="逍遥游: 当您执行“升沉”移动时，所需消耗的AP永久-1（最低为1 AP）。"
)

def setup_game() -> GameState:
    """Sets up the initial game state for a 2-player game."""
    player1 = Player(name="Alice", avatar=EMPEROR_AVATAR)
    player2 = Player(name="Bob", avatar=HERMIT_AVATAR)

    # Give each player a copy of the same card for testing
    player1.hand.append(QIAN_WEI_TIAN)
    player2.hand.append(QIAN_WEI_TIAN)

    return GameState(players=[player1, player2])

def main_game_loop():
    """The main loop for the game CLI."""
    game_state = setup_game()
    turn_limit = 20 # Add a limit to prevent infinite loops in prototype

    while game_state.turn <= turn_limit:
        player = game_state.get_current_player()

        print("\n" + "="*50)
        print(game_state) # Use the __str__ method from GameState

        print(f"--- {player.name}'s Hand ---")
        for i, card in enumerate(player.hand):
            print(f"  [{i}] {card.name}")

        if player.current_task_card:
            print(f"--- Active Task Card: {player.current_task_card.name} ---")
            for i, task in enumerate(player.current_task_card.tasks):
                print(f"  [{i}] {task.name} ({task.level})")

        print("="*50)

        # Simple command parser
        action_input = input("Action> ").strip().lower().split()
        if not action_input:
            continue

        command = action_input[0]
        args = action_input[1:]

        action_taken = False
        try:
            if command == "play" and len(args) == 2:
                card_idx = int(args[0])
                zone_choice = args[1] # Keep the original input for Chinese characters
                action_taken = actions.play_card(game_state, card_idx, zone_choice)

            elif command == "move" and len(args) == 1:
                zone_str = args[0]
                action_taken = actions.move(game_state, zone_str)

            elif command == "task" and len(args) == 1:
                task_idx = int(args[0])
                action_taken = actions.complete_task(game_state, task_idx)

            elif command == "pass":
                print(f"{player.name} passes the turn.")
                action_taken = True

            elif command == "exit":
                print("Exiting game.")
                break

            else:
                print("Unknown command. Use: play <card#> <zone>, move <zone>, task <task#>, pass, exit")

        except (ValueError, IndexError) as e:
            print(f"Invalid command arguments: {e}")


        # Advance to next player if an action was successfully taken
        if action_taken:
            game_state.current_player_index = (game_state.current_player_index + 1) % len(game_state.players)
            # Increment turn number when all players have had a turn
            if game_state.current_player_index == 0:
                game_state.turn += 1

    print("\nGame has ended (turn limit reached).")

if __name__ == "__main__":
    main_game_loop()
