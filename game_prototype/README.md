# 《天机变·周天纪》 - Python Prototype Documentation

This document explains the structure and design of the Python-based command-line prototype for the board game 《天机变·周天纪》.

## How to Run

To run the prototype, execute the following command from the repository's root directory:
```bash
python3 game_prototype/main.py
```

## Project Structure

The prototype is organized into four main files, each with a specific responsibility:

-   `main.py`: **Game Entry Point & CLI**
    -   This is the main executable file.
    -   It contains the primary game loop (`main_game_loop`) which handles player turns.
    -   It is responsible for setting up the initial game state (creating players and avatars).
    -   It manages the command-line interface (CLI), printing the game state and parsing user input.

-   `game_state.py`: **Core Data Structures**
    -   This file defines the foundational data classes that represent the game's state.
    -   `GameState`: The main container class that holds all information about the current game (players, board, turn number).
    -   `GameBoard`: Represents the physical board, including the 8 Gua zones and player positions.
    -   `Player`: Holds all information for a single player, such as their hand, resources (`dao_xing`, `cheng_yi`), and active task card.
    -   `Avatar`: Defines the player's role (e.g., "帝王", "隐士").

-   `actions.py`: **Game Logic & Player Actions**
    -   This file contains the functions that modify the game state.
    -   Each function (e.g., `play_card`, `move`, `complete_task`) corresponds to a specific action a player can take.
    -   These functions are designed to be "pure" in the sense that they take the current `game_state` as input and return a boolean indicating success, modifying the state object directly. This keeps the main loop in `main.py` clean.

-   `cards.py`: **Card and Task Definitions**
    -   This file defines the data structures for the game's cards.
    -   `GuaCard`: Represents a single卦 card, containing its name and a list of 6 tasks.
    -   `YaoCiTask`: A simple data structure (NamedTuple) to hold the details of a single task.
    -   This file also acts as a "card database", where specific cards like `QIAN_WEI_TIAN` are defined and collected into the `GAME_DECK`.

## Core Design Philosophy

-   **State-Action Separation:** The design separates the game's *state* (`game_state.py`) from its *logic* (`actions.py`). The `main.py` file acts as the controller, taking user input and using the logic functions to modify the state. This makes the code easier to test and maintain.
-   **Data-Driven Cards:** The card and task system in `cards.py` is data-driven. To add new cards to the game, one only needs to define a new `GuaCard` instance and add it to the `GAME_DECK`. No changes to the core logic should be necessary for simple additions.
-   **Simplicity for Prototyping:** This prototype omits several complex features (e.g., AP costs, detailed task effects, avatar abilities) for the sake of simplicity. The focus is on providing a functional core that demonstrates the main gameplay loop. The `print()` statements in the action functions serve as a basic form of logging to show the game's flow.
