import tkinter as tk
import threading
import time
import random as rnd

class PixelMap:
    def __init__(self, master, width, height, pixel_size, map):
        self.master = master
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.map = map

        self.isRunning = True

        self.players = set()
        self.players_lock = threading.Lock()
        self.canvas_lock = threading.Lock()
        self.position_locks = {}

        self.canvas = tk.Canvas(master, width=width*pixel_size, height=height*pixel_size)
        self.canvas.pack()

        self.draw_map()

        self.treasure_position = None
        self.treasure_lock = threading.Lock()
        self.spawn_treasure()

        self.human_player1 = [rnd.randint(3, self.width-4), rnd.randint(3, self.height-4)]
        self.human_player2 = [rnd.randint(3, self.width-4), rnd.randint(3, self.height-4)]

        self.human_player1_picking = False
        self.human_player2_picking = False

        self.player1_cooldown = False
        self.player2_cooldown = False

        self.player1_score = 0
        self.player2_score = 0

        self.score_label = tk.Label(master, text=f"Player 1: {self.player1_score}  Player 2: {self.player2_score}")
        self.score_label.pack()

        self.move_player_thread1 = threading.Thread(target=self.start_press_listener1)
        self.move_player_thread2 = threading.Thread(target=self.start_press_listener2)
        self.move_player_thread1.start()
        self.move_player_thread2.start()

        self.display_player(self.human_player1, "red")
        self.display_player(self.human_player2, "blue")

    def draw_map(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.map[i][j] == 'W':
                    color = "black"
                elif self.map[i][j] == 'F':
                    color = "grey"

                self.canvas.create_rectangle(
                    i*self.pixel_size,
                    j*self.pixel_size,
                    (i+1)*self.pixel_size,
                    (j+1)*self.pixel_size,
                    fill=color
                )
                self.position_locks[f"{i}_{j}"] = threading.Lock()

    def spawn_treasure(self):
        if self.treasure_position:
            x, y = self.treasure_position
            self.canvas.create_rectangle(
                x*self.pixel_size,
                y*self.pixel_size,
                (x+1)*self.pixel_size,
                (y+1)*self.pixel_size,
                fill="grey"
            )
        while True:
            x = rnd.randint(1, self.width-1)
            y = rnd.randint(1, self.height-1)
            new_position = f"{x}_{y}"
            if self.map[x][y] == 'F' and new_position not in self.players:
                break

        self.treasure_position = [x, y]
        self.canvas.create_rectangle(
            x*self.pixel_size,
            y*self.pixel_size,
            (x+1)*self.pixel_size,
            (y+1)*self.pixel_size,
            fill="yellow"
        )

    def move_player(self, x, y, direction):
        new_position = [x, y]
        if direction == -1:
            return [x, y]

        if direction == 0 and y > 1:
            new_position[1] -= 1
        elif direction == 1 and x < self.width-2:
            new_position[0] += 1
        elif direction == 2 and y < self.height-2:
            new_position[1] += 1
        elif direction == 3 and x > 1:
            new_position[0] -= 1

        if self.treasure_position and self.treasure_position[0] == new_position[0] and self.treasure_position[1] == new_position[1]:
            return [x, y]

        target_position = f"{new_position[0]}_{new_position[1]}"
        
        with self.position_locks[target_position]:
            with self.players_lock:
                if target_position not in self.players:
                    self.players.discard(f"{x}_{y}")
                    self.players.add(target_position)
                    with self.canvas_lock:
                        self.canvas.create_rectangle(
                            x*self.pixel_size,
                            y*self.pixel_size,
                            (x+1)*self.pixel_size,
                            (y+1)*self.pixel_size,
                            fill="grey"
                        )
                        if [x, y] == self.human_player1:
                            color = "red"
                            self.human_player1 = new_position
                        elif [x, y] == self.human_player2:
                            color = "blue"
                            self.human_player2 = new_position
                        else:
                            color = "green"
                        self.canvas.create_rectangle(
                            new_position[0]*self.pixel_size,
                            new_position[1]*self.pixel_size,
                            (new_position[0]+1)*self.pixel_size,
                            (new_position[1]+1)*self.pixel_size,
                            fill=color
                        )
                    return new_position
        return [x, y]

    def display_player(self, position, color):
        x, y = position
        self.canvas.create_rectangle(
            x*self.pixel_size,
            y*self.pixel_size,
            (x+1)*self.pixel_size,
            (y+1)*self.pixel_size,
            fill=color
        )
        self.players.add(f"{x}_{y}")

    def update_score(self):
        self.score_label.config(text=f"Player 1: {self.player1_score}  Player 2: {self.player2_score}")

    def on_press1(self, event):
        if self.human_player1_picking or self.player1_cooldown:
            return
        try:
            direction = -1
            if event.keysym == 'Up':
                direction = 0
            elif event.keysym == 'Right':
                direction = 1
            elif event.keysym == 'Down':
                direction = 2
            elif event.keysym == 'Left':
                direction = 3
            elif event.keysym == 'space' and not self.human_player2_picking:
                self.attempt_pickup_treasure(self.human_player1, 1)
            self.human_player1 = self.move_player(self.human_player1[0], self.human_player1[1], direction)
        except AttributeError:
            pass

    def on_press2(self, event):
        if self.human_player2_picking or self.player2_cooldown:
            return
        try:
            direction = -1
            if event.keysym == 'w':
                direction = 0
            elif event.keysym == 'd':
                direction = 1
            elif event.keysym == 's':
                direction = 2
            elif event.keysym == 'a':
                direction = 3
            elif event.keysym == 'Return' and not self.human_player1_picking:
                self.attempt_pickup_treasure(self.human_player2, 2)
            self.human_player2 = self.move_player(self.human_player2[0], self.human_player2[1], direction)
        except AttributeError:
            pass

    def start_press_listener1(self):
        self.master.bind("<Up>", self.on_press1)
        self.master.bind("<Down>", self.on_press1)
        self.master.bind("<Left>", self.on_press1)
        self.master.bind("<Right>", self.on_press1)
        self.master.bind("<space>", self.on_press1)

    def start_press_listener2(self):
        self.master.bind("<w>", self.on_press2)
        self.master.bind("<s>", self.on_press2)
        self.master.bind("<a>", self.on_press2)
        self.master.bind("<d>", self.on_press2)
        self.master.bind("<Return>", self.on_press2)

    def attempt_pickup_treasure(self, player_position, player_id):
        with self.treasure_lock:
            if self.treasure_position:
                tx, ty = self.treasure_position
                px, py = player_position
                if abs(tx - px) <= 1 and abs(ty - py) <= 1:
                    if player_id == 1:
                        self.human_player1_picking = True
                        self.player1_cooldown = True
                        self.player1_score += 1
                    elif player_id == 2:
                        self.human_player2_picking = True
                        self.player2_cooldown = True
                        self.player2_score += 1
                    self.update_score()
                    threading.Thread(target=self.pickup_treasure, args=(player_id,)).start()

    def pickup_treasure(self, player_id):
        with self.treasure_lock:
            self.remove_treasure()
        time.sleep(3)  # 3 seconds cooldown
        if player_id == 1:
            self.human_player1_picking = False
            self.player1_cooldown = False
        elif player_id == 2:
            self.human_player2_picking = False
            self.player2_cooldown = False
        self.spawn_treasure()

    def remove_treasure(self):
        if self.treasure_position:
            x, y = self.treasure_position
            self.canvas.create_rectangle(
                x*self.pixel_size,
                y*self.pixel_size,
                (x+1)*self.pixel_size,
                (y+1)*self.pixel_size,
                fill="grey"
            )
            self.treasure_position = None

    def close(self):
        self.isRunning = False
        self.move_player_thread1.join()
        self.move_player_thread2.join()

def read_map(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            map = []
            for line in lines:
                line_to_chars = [char for char in line if char != '\n']
                map.append(line_to_chars)
            return map
    except FileNotFoundError:
        print("Nie znaleziono pliku o podanej nazwie.")
        return None

def on_closing(map):
    map.close()
    exit()

def main():
    root = tk.Tk()
    root.title("Pixel Map")
    map = read_map("base_map.txt")
    if map is not None:
        pixel_map = PixelMap(master=root, height=len(map), width=len(map[0]), pixel_size=16, map=map)
        root.protocol("WM_DELETE_WINDOW", lambda: on_closing(pixel_map))
        root.mainloop()

if __name__ == "__main__":
    main()
