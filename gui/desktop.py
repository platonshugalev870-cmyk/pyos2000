import tkinter as tk
from tkinter import messagebox
from apps.notepad import Notepad
from apps.calculator import Calculator
from apps.explorer import Explorer
from apps.paint import Paint
from apps.minesweeper import Minesweeper
from apps.physics.physics import PhysicsApp
from apps.history.history import HistoryApp
from utils.animate import fade_in_window, gui_type_lines


class Desktop:
    def __init__(self, logger, colors, vfs, registry):
        self.logger = logger
        self.colors = colors
        self.vfs = vfs
        self.registry = registry
        self.root = None
        self.icon_widgets = []

    def run(self):
        self.root = tk.Tk()
        self.root.title("PyOS 2000")
        self.root.geometry("900x600")
        self.root.configure(bg="#008080")
        self.build_desktop()
        self.build_taskbar()
        fade_in_window(self.root, steps=14, delay=25)
        self.animate_icons()
        self.root.mainloop()

    def build_desktop(self):
        desktop = tk.Frame(self.root, bg="#008080")
        desktop.pack(fill="both", expand=True)
        icons = [
            ("My Computer", "🖥", 20, 20, self.open_explorer),
            ("Notepad", "📝", 20, 130, self.open_notepad),
            ("Calculator", "🧮", 20, 240, self.open_calculator),
            ("Paint", "🎨", 20, 350, self.open_paint),
            ("Minesweeper", "💣", 20, 460, self.open_minesweeper),
            ("Physics Lab", "⚛", 140, 20, self.open_physics),
            ("History", "📜", 140, 130, self.open_history),
        ]
        for label, symbol, x, y, cb in icons:
            w = self.build_icon(desktop, label, symbol, x, y, cb)
            w.place_forget()
            self.icon_widgets.append((w, x, y))

    def build_icon(self, parent, label, symbol, x, y, callback):
        icon = tk.Frame(parent, bg="#008080")
        icon.place(x=x, y=y)
        btn = tk.Label(
            icon, text=symbol, font=("Arial", 28),
            bg="#008080", fg="white", cursor="hand2"
        )
        btn.pack()
        btn.bind("<Double-Button-1>", lambda e: callback())
        tk.Label(
            icon, text=label, font=("Arial", 9),
            bg="#008080", fg="white"
        ).pack()
        return icon

    def animate_icons(self):
        state = {"i": 0}

        def step():
            if state["i"] >= len(self.icon_widgets):
                return
            w, x, y = self.icon_widgets[state["i"]]
            w.place(x=x, y=y)
            state["i"] += 1
            self.root.after(80, step)

        self.root.after(200, step)

    def build_taskbar(self):
        bar = tk.Frame(self.root, bg="#c0c0c0", height=34)
        bar.pack(side="bottom", fill="x")
        bar.pack_propagate(False)
        tk.Button(
            bar, text="  Start  ", font=("Arial", 10, "bold"),
            bg="#c0c0c0", relief="raised",
            command=self.show_start_menu
        ).pack(side="left", padx=2, pady=2)
        self.clock = tk.Label(
            bar, text="", font=("Arial", 10),
            bg="#c0c0c0", fg="black"
        )
        self.clock.pack(side="right", padx=10)
        self.tick_clock()

    def tick_clock(self):
        import time
        self.clock.config(text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self.tick_clock)

    def show_start_menu(self):
        menu = tk.Toplevel(self.root)
        menu.title("Start")
        menu.geometry("230x340+0+560")
        menu.overrideredirect(True)
        menu.configure(bg="#c0c0c0")
        items = [
            ("Notepad", self.open_notepad),
            ("Calculator", self.open_calculator),
            ("Explorer", self.open_explorer),
            ("Paint", self.open_paint),
            ("Minesweeper", self.open_minesweeper),
            ("Physics Lab", self.open_physics),
            ("History Archive", self.open_history),
            ("", None),
            ("Shut Down...", self.shutdown),
        ]
        for name, cb in items:
            if cb is None:
                tk.Frame(menu, bg="#808080", height=1).pack(fill="x", pady=4)
                continue
            tk.Button(
                menu, text=name, anchor="w", width=24,
                font=("Arial", 10), bg="#c0c0c0", relief="flat",
                command=lambda c=cb, m=menu: (m.destroy(), c())
            ).pack(fill="x", padx=4, pady=1)
        fade_in_window(menu, steps=8, delay=20)

    def shutdown(self):
        if messagebox.askyesno("PyOS 2000", "Are you sure you want to shut down?"):
            self.root.destroy()

    def open_notepad(self):
        Notepad(self.root, self.vfs).run()

    def open_calculator(self):
        Calculator(self.root).run()

    def open_explorer(self):
        Explorer(self.root, self.vfs).run()

    def open_paint(self):
        Paint(self.root).run()

    def open_minesweeper(self):
        Minesweeper(self.root).run()

    def open_physics(self):
        PhysicsApp(self.root).run()

    def open_history(self):
        HistoryApp(self.root).run()