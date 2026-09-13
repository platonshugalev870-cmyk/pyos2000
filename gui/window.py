import tkinter as tk
from utils.animate import fade_in_window, slide_in_window


class PyWindow:
    def __init__(self, parent, title, width=500, height=400):
        self.win = tk.Toplevel(parent)
        self.win.title(title)
        self.win.geometry(f"{width}x{height}")
        self.win.configure(bg="#c0c0c0")
        titlebar = tk.Frame(self.win, bg="#000080", height=28)
        titlebar.pack(fill="x")
        titlebar.pack_propagate(False)
        tk.Label(
            titlebar, text=title, bg="#000080", fg="white",
            font=("Arial", 10, "bold")
        ).pack(side="left", padx=8)
        tk.Button(
            titlebar, text="X", bg="#c0c0c0", fg="black",
            font=("Arial", 9, "bold"), width=2,
            command=self.win.destroy
        ).pack(side="right", padx=4, pady=3)
        self.body = tk.Frame(self.win, bg="#c0c0c0")
        self.body.pack(fill="both", expand=True, padx=6, pady=6)
        self.win.update_idletasks()
        x = self.win.winfo_x()
        y = self.win.winfo_y()
        fade_in_window(self.win, steps=10, delay=25)
        slide_in_window(self.win, x, y, steps=10, delay=12)