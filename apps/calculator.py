import tkinter as tk
from gui.window import PyWindow


class Calculator:
    def __init__(self, parent):
        self.parent = parent
        self.expr = ""

    def run(self):
        w = PyWindow(self.parent, "Калькулятор", 260, 340)
        display = tk.Entry(w.body, font=("Consolas", 16), justify="right")
        display.pack(fill="x", pady=(0, 8))

        def press(ch):
            self.expr += ch
            display.delete(0, "end")
            display.insert(0, self.expr)

        def clear():
            self.expr = ""
            display.delete(0, "end")

        def equals():
            try:
                result = str(eval(self.expr))
            except Exception:
                result = "Error"
            display.delete(0, "end")
            display.insert(0, result)
            self.expr = result if result != "Error" else ""

        grid = tk.Frame(w.body)
        grid.pack()
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
        ]
        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                cmd = equals if label == "=" else (lambda ch=label: press(ch))
                tk.Button(
                    grid, text=label, width=5, height=2,
                    font=("Arial", 11, "bold"), command=cmd
                ).grid(row=r, column=c, padx=2, pady=2)
        tk.Button(
            w.body, text="C", width=22, height=2,
            font=("Arial", 11, "bold"), bg="#ff8080", command=clear
        ).pack(pady=6)