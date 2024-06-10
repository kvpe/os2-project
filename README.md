# Treasure Hunting Game

Project done for Operating Systems 2 course.
The goal of the project is to create an application with GUI, that incorporates threading.

## Concept Image:

![alt text](https://raw.githubusercontent.com/kvpe/os2-project/main/game_picture.png)

## Project Description

The Treasure Hunting Game involves two human players navigating a grid-based map to collect randomly spawned treasures. The players move using keyboard controls and compete to see who can collect the most treasures within the game session. The game includes a simple graphical interface, a scoreboard, and utilizes threading to handle concurrent player actions and treasure management. This project is a graphical game implemented in Python using the Tkinter library. The game features a pixel map where two human players can move around and compete to collect treasures.

## Installation and running

Ensure you have Python installed on your system!!

Install the Tkinter library if not already installed:

```
bash
pip install tk
```

Download the repository and navigate to the project directory.

(Optional) Prepare a map file (base_map.txt) with the following format:

```
Use 'W' for walls.
Use 'F' for free spaces.
```

You can now run the game using the following command:

```
python main.py
```

## Gameplay

Control the players using the keyboard:
Player 1: Arrow keys to move, Space to pick up treasure.
Player 2: WASD keys to move, Enter to pick up treasure.
Treasures are colored yellow, player one is red, and player two is blue.

#### Controls

## Player 1:

```
*Up*: Up Arrow
*Down*: Down Arrow
*Left*: Left Arrow
*Right*: Right Arrow
*Pick up treasure*: Space
```

## Player 2:

```
*Up*: W
*Down*: S
*Left*: A
*Right*: D
*Pick up treasure*: Enter
```

Players navigate the map, searching the treasures. Player can only pick up the treasure when he is on a tile adjacent to treasure.
Players cannot walk into tiles occupied by other players, and treasures.
Action of picking up the treasure takes 5 seconds.
When a treasure is being picked up by a player, the player that is picking up the treasure cannot perform any other actions.
When a treasure is being picked up by a player, other players cannot pick it up.

## Threads

We used 3 different threads in order for the game to be able to be played by two players, who can pick up treasures

```
*move_player_thread1*: Handles the movement and actions of Player 1.
*move_player_thread2*: Handles the movement and actions of Player 2.
*pickup_treasure*: Manages the treasure pickup process and cooldown period.
```

## Critical Sections

```
*self.players_lock* - Mutex lock that protects the self.players set which keeps track of player positions. This ensures that only one thread can add or remove player positions from the set at a time.
```

```
*self.canvas_lock* - Mutex lock that ensures thread-safe operations on the Tkinter canvas. Since Tkinter is not thread-safe, any updates to the canvas are protected by this lock.
```

```
*self.position_locks* - A dictionary of mutex locks for each map position to manage concurrent access. Each position on the map has its own lock to ensure that no two players can move to the same position simultaneously.
```

```
*self.treasure_lock* - Mutex lock that manages access to the treasure position, ensuring it can only be altered by one thread at a time. This lock prevents race conditions when checking and updating the treasure's position.
```

## Listings of thread initialization

```py

self.move_player_thread1 = threading.Thread(target=self.start_press_listener1)

self.move_player_thread2 = threading.Thread(target=self.start_press_listener2)

threading.Thread(target=self.pickup_treasure, args=(player_id,)).start()
```

Both player threads start at the beginning. They run continuusly, until the game is stopped.

Thread responsible for picking up the treasure is started when the player succeeds an attempt to pick up a treasure.
Its terminated after the player finishes picking the treasure up.
