import random
import tkinter as tk
from tkinter import messagebox
from gui.window import PyWindow


class Minesweeper:
    def __init__(self, parent):
        self.parent = parent
        self.width = 12
        self.height = 10
        self.mines = 15
        self.buttons = {}
        self.revealed = set()
        self.flagged = set()
        self.mine_positions = set()

    def run(self):
        self.win = PyWindow(self.parent, "Minesweeper", 480, 440)
        self.grid = tk.Frame(self.win.body)
        self.grid.pack(pady=6)
        self.status = tk.Label(self.win.body, text="Left click to dig, right click to flag", bg="#c0c0c0")
        self.status.pack()
        self.reset()

    def reset(self):
        for b in self.buttons.values():
            b.destroy()
        self.buttons.clear()
        self.revealed.clear()
        self.flagged.clear()
        self.mine_positions.clear()
        placed = 0
        while placed < self.mines:
            pos = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if pos not in self.mine_positions:
                self.mine_positions.add(pos)
                placed += 1
        for y in range(self.height):
            for x in range(self.width):
                b = tk.Button(self.grid, width=3, height=1, font=("Arial", 10, "bold"))
                b.grid(row=y, column=x)
                b.bind("<Button-1>", lambda e, x=x, y=y: self.dig(x, y))
                b.bind("<Button-3>", lambda e, x=x, y=y: self.flag(x, y))
                self.buttons[(x, y)] = b

    def neighbors(self, x, y):
        out = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    out.append((nx, ny))
        return out

    def dig(self, x, y):
        if (x, y) in self.revealed or (x, y) in self.flagged:
            return
        if (x, y) in self.mine_positions:
            for p in self.mine_positions:
                self.buttons[p].config(text="*", bg="#ff4040")
            self.status.config(text="BOOM! You lose.")
            return
        self.reveal(x, y)
        self.check_win()

    def reveal(self, x, y):
        if (x, y) in self.revealed:
            return
        self.revealed.add((x, y))
        cnt = sum(1 for n in self.neighbors(x, y) if n in self.mine_positions)
        b = self.buttons[(x, y)]
        b.config(bg="#d0d0d0", relief="sunken")
        if cnt:
            b.config(text=str(cnt), fg=["", "blue", "green", "red", "purple", "brown", "cyan", "black", "gray"][cnt])
        else:
            for n in self.neighbors(x, y):
                self.reveal(*n)

    def flag(self, x, y):
        if (x, y) in self.revealed:
            return
        b = self.buttons[(x, y)]
        if (x, y) in self.flagged:
            self.flagged.remove((x, y))
            b.config(text="")
        else:
            self.flagged.add((x, y))
            b.config(text="F", fg="red")

    def check_win(self):
        if len(self.revealed) == self.width * self.height - self.mines:
            self.status.config(text="You win!")
            messagebox.showinfo("Minesweeper", "You win!")