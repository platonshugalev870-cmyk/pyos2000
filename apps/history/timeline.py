import tkinter as tk
from apps.history.data import EPOCH_LABELS


class Timeline:
    def __init__(self, parent, events):
        self.parent = parent
        self.events = sorted(events, key=lambda e: e["year"])
        self.canvas = None
        self.tooltip = None

    def build(self, container):
        self.canvas = tk.Canvas(
            container, bg="#1a1a2e", height=140, highlightthickness=0
        )
        self.canvas.pack(fill="x", padx=6, pady=6)
        self.canvas.bind("<Configure>", lambda e: self.draw())
        self.canvas.bind("<Motion>", self.on_motion)
        self.canvas.bind("<Leave>", self.hide_tooltip)
        self.tooltip = tk.Label(
            container, text="", bg="#ffffe0", fg="#000000",
            font=("Arial", 9), relief="solid", bd=1
        )

    def draw(self):
        c = self.canvas
        c.delete("all")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 10 or not self.events:
            return
        years = [e["year"] for e in self.events]
        ymin, ymax = min(years), max(years)
        span = ymax - ymin or 1
        margin = 40
        usable = w - 2 * margin
        line_y = h // 2 + 15
        c.create_line(margin, line_y, w - margin, line_y, fill="#707080", width=3)
        for i in range(0, 11):
            x = margin + usable * i / 10
            c.create_line(x, line_y - 4, x, line_y + 4, fill="#505060")
        self.positions = []
        for e in self.events:
            x = margin + usable * (e["year"] - ymin) / span
            color = EPOCH_LABELS.get(e["era"], "#ffffff")
            c.create_oval(x - 6, line_y - 6, x + 6, line_y + 6, fill=color, outline="#ffffff", width=1)
            c.create_text(
                x, line_y + 18, text=e["label"],
                fill="#c0c0d0", font=("Arial", 7), angle=0
            )
            self.positions.append((x, line_y, e))

    def on_motion(self, event):
        if not hasattr(self, "positions"):
            return
        closest = None
        best = 15
        for x, y, e in self.positions:
            d = abs(event.x - x)
            if d < best:
                best = d
                closest = (x, y, e)
        if closest:
            x, y, e = closest
            text = f"{e['label']} — {e['title']}"
            self.tooltip.config(text=text)
            self.tooltip.place(x=x - 80, y=y - 50)
        else:
            self.hide_tooltip()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.place_forget()