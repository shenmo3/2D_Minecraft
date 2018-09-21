from tkinter import *
import random

WORLD_WIDTH = 800
WORLD_HEIGHT = 600


# dirt = 1, water = 2, grass = 3
class Display:
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=WORLD_WIDTH, height=WORLD_HEIGHT + 100)
        self.canvas.pack()
        self.world = World()
        self.root.bind("<KeyPress>", self.key_press)

    def start(self):
        self.world.start()
        self.refresh()
        self.root.mainloop()

    def draw_game(self):
        self.canvas.create_rectangle(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
        for idx, i in enumerate(self.world.object):
            for jidx, j in enumerate(i):
                if j == 1:
                    self.canvas.create_rectangle(jidx * 25, idx * 25, jidx * 25 + 25, idx * 25 + 25, fill="brown")
                elif j == 2:
                    self.canvas.create_rectangle(jidx * 25, idx * 25, jidx * 25 + 25, idx * 25 + 25, fill="blue")
                elif j == 3:
                    self.canvas.create_rectangle(jidx * 25, idx * 25, jidx * 25 + 25, idx * 25 + 25, fill="green")
        self.canvas.create_oval(self.world.player.x * 25, self.world.player.y * 25, self.world.player.x * 25 + 25,
                                self.world.player.y * 25 + 25, fill="white")

    def key_press(self, event):
        if event.keysym == "w":
            self.world.player.change_direction("Up")
        elif event.keysym == "s":
            self.world.player.change_direction("Down")
        elif event.keysym == "a":
            self.world.player.change_direction("Left")
        elif event.keysym == "d":
            self.world.player.change_direction("Right")
        elif event.keysym == "space":
            self.world.pick()
        elif event.keysym == "1":
            self.world.place(1)
        elif event.keysym == "2":
            self.world.place(2)
        elif event.keysym == "3":
            self.world.place(3)
        else:
            print("Invalid Input")

    def refresh(self):
        self.world.refresh()
        self.canvas.delete('all')
        self.draw_game()
        self.root.after(10, self.refresh)


class World:
    def __init__(self):
        self.width = int(WORLD_WIDTH / 25)
        self.height = int(WORLD_HEIGHT / 25)
        self.object = []
        self.player = Player()

    def start(self):
        for i in range(self.height):
            temp = []
            for i in range(self.width):
                temp.append(1)
            self.object.append(temp)
        for i in range(random.randint(250, 350)):
                self.object[random.randint(0, 23)][random.randint(0, 31)] = 3
        for i in range(random.randint(50, 100)):
            self.object[random.randint(0, 23)][random.randint(0, 31)] = 2

    def pick(self):
        self.player.pick(self.object[self.player.y][self.player.x])
        self.object[self.player.y][self.player.x] = 1

    def place(self, num):
        if self.player.place(num):
            self.object[self.player.y][self.player.x] = num

    def refresh(self):
        pass


class Player:
    def __init__(self):
        self.width = int(WORLD_WIDTH / 25)
        self.height = int(WORLD_HEIGHT / 25)
        self.x = random.randint(0, 31)
        self.y = random.randint(0, 23)
        # [dirt, water, grass]
        self.inventory = [0, 0, 0]

    def change_direction(self, direction):
        if direction == "Up":
            self.y = self.y - 1
        elif direction == "Down":
            self.y = self.y + 1
        elif direction == "Left":
            self.x = self.x - 1
        elif direction == "Right":
            self.x = self.x + 1

    def pick(self, num):
        self.inventory[num - 1] += 1

    def place(self, num):
        if self.inventory[num - 1] > 0:
            self.inventory[num - 1] -= 1
            return True
        return False


if __name__ == "__main__":
    d = Display()
    d.start()
