import tkinter as tk
from tkinter import colorchooser
from gui.window import PyWindow


class Paint:
    def __init__(self, parent):
        self.parent = parent
        self.color = "black"
        self.last_x = None
        self.last_y = None

    def run(self):
        w = PyWindow(self.parent, "Paint", 700, 520)
        canvas = tk.Canvas(w.body, bg="white", width=660, height=400)
        canvas.pack(pady=6)

        def start(e):
            self.last_x = e.x
            self.last_y = e.y

        def draw(e):
            if self.last_x is None:
                return
            canvas.create_line(
                self.last_x, self.last_y, e.x, e.y,
                fill=self.color, width=2, capstyle="round"
            )
            self.last_x = e.x
            self.last_y = e.y

        def stop(e):
            self.last_x = None
            self.last_y = None

        def pick():
            c = colorchooser.askcolor()[1]
            if c:
                self.color = c

        canvas.bind("<Button-1>", start)
        canvas.bind("<B1-Motion>", draw)
        canvas.bind("<ButtonRelease-1>", stop)
        bar = tk.Frame(w.body)
        bar.pack(fill="x")
        tk.Button(bar, text="Color", width=10, command=pick).pack(side="left", padx=4)
        tk.Button(bar, text="Clear", width=10, command=lambda: canvas.delete("all")).pack(side="left", padx=4)