import tkinter as tk
import threading
import time
import random as rnd

class PixelMap :
    def __init__(self, master, width, height, pixel_size, map):
        self.master = master
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.map = map

        self.players = [];
        self.canvas = tk.Canvas(master, width=width*pixel_size, height=height*pixel_size)
        self.canvas.pack()

        self.move_players_threads = []

        self.draw_map()

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
        
    def add_player(self):
        new_player = [rnd.randint(3, self.width-4), rnd.randint(3, self.height-4)]
        self.players.append(new_player)
        index = len(self.move_players_threads)
        new_thread = threading.Thread(target=self.move_player_index, args=(index,))
        self.move_players_threads.append(new_thread)
        self.move_players_threads[index].start()
        

    def move_player(self, player, direction):
        # 0 - up, 1 - right, 2 - down, 3 - left
        self.canvas.create_rectangle(
                player[0]*self.pixel_size,
                player[1]*self.pixel_size,
                (player[0]+1)*self.pixel_size,
                (player[1]+1)*self.pixel_size,
                fill="grey"
            )
        if direction == 0:
            if player[1] > 2:
                player[1] -= 1
        elif direction == 1:
            if player[0] < self.width-3:
                player[0] += 1
        elif direction == 2:
            if player[1] < self.height-3:
                player[1] += 1
        elif direction == 3:
            if player[0] > 2:
                player[0] -= 1
        for player in self.players:
            self.canvas.create_rectangle(
                player[0]*self.pixel_size,
                player[1]*self.pixel_size,
                (player[0]+1)*self.pixel_size,
                (player[1]+1)*self.pixel_size,
                fill="red"
            )

    def move_player_index(self,index):
        while True:
            time.sleep(0.5)
            self.move_player(self.players[index], rnd.randint(0, 3))

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
    
def main():
    root = tk.Tk()
    root.title("Pixel Map")

    map = read_map("base_map.txt")
    if map is not None:
        pixel_map = PixelMap(master=root, height=len(map), width=len(map[0]), pixel_size=6, map=map)
        time.sleep(1)
        pixel_map.add_player()
        time.sleep(1)
        pixel_map.add_player()
        root.mainloop()

if __name__ == "__main__":
    main()