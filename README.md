# Treasure Hunting Game

Project done for Operating Systems 2 course.
The goal of the project is to create an application with GUI, that incorporates threading.

We used Poetry as our package manager. To install poetry run

```
pip install poetry
```

on your terminal.

To then install required packages run

```
poetry install
```

Concept Image:

Project Description

The Treasure Hunting Game involves two human players navigating a grid-based map to collect randomly spawned treasures. The players move using keyboard controls and compete to see who can collect the most treasures within the game session. The game includes a simple graphical interface, a scoreboard, and utilizes threading to handle concurrent player actions and treasure management. This project is a graphical game implemented in Python using the Tkinter library. The game features a pixel map where two human players can move around and compete to collect treasures. The game demonstrates the use of threading, critical sections, and Tkinter for GUI development.
Installation

    Ensure you have Python installed on your system.
    Install the Tkinter library if not already installed:

    bash

    pip install tk

    Download the repository and navigate to the project directory.

Usage

    Prepare a map file (base_map.txt) with the following format:
        Use 'W' for walls.
        Use 'F' for free spaces.
    Run the main script:

    bash

    python pixel_map_game.py

    Control the players using the keyboard:
        Player 1: Arrow keys to move, Space to pick up treasure.
        Player 2: WASD keys to move, Enter to pick up treasure.

Controls

    Player 1:
        Up: Up Arrow
        Down: Down Arrow
        Left: Left Arrow
        Right: Right Arrow
        Pick up treasure: Space
    Player 2:
        Up: W
        Down: S
        Left: A
        Right: D
        Pick up treasure: Enter

Threads

    move_player_thread1: Handles the movement and actions of Player 1.
    move_player_thread2: Handles the movement and actions of Player 2.
    pickup_treasure: Manages the treasure pickup process and cooldown period.

Critical Sections

self.players_lock: Mutex lock that protects the self.players set which keeps track of player positions. This ensures that only one thread can add or remove player positions from the set at a time.


self.canvas_lock: Mutex lock that ensures thread-safe operations on the Tkinter canvas. Since Tkinter is not thread-safe, any updates to the canvas are protected by this lock.



self.position_locks: A dictionary of mutex locks for each map position to manage concurrent access. Each position on the map has its own lock to ensure that no two players can move to the same position simultaneously.



self.treasure_lock: Mutex lock that manages access to the treasure position, ensuring it can only be altered by one thread at a time. This lock prevents race conditions when checking and updating the treasure's position.


Code Overview
Main Classes and Functions
PixelMap

    __init__: Initializes the game, creates threads, and sets up the GUI.
    draw_map: Draws the initial map based on the input file.
    spawn_treasure: Randomly spawns a treasure on the map.
    move_player: Moves a player in the specified direction if the move is valid.
    display_player: Displays a player on the map at the specified position.
    update_score: Updates the scoreboard with the current scores.
    on_press1: Handles key press events for Player 1.
    on_press2: Handles key press events for Player 2.
    start_press_listener1: Binds keys to actions for Player 1.
    start_press_listener2: Binds keys to actions for Player 2.
    attempt_pickup_treasure: Initiates the treasure pickup process for a player.
    pickup_treasure: Handles the cooldown period after a player picks up a treasure.
    remove_treasure: Removes the treasure from the map.
    close: Stops the game and joins threads.

read_map

    Reads the map file and returns the map as a list of lists.

on_closing

    Closes the game safely.

main

    The main entry point of the game, initializes and starts the Tkinter main loop.
