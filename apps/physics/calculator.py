import tkinter as tk
from tkinter import messagebox
from gui.window import PyWindow


class FormulaCalculator:
    def __init__(self, parent, formula, solver):
        self.parent = parent
        self.formula = formula
        self.solver = solver

    def run(self):
        w = PyWindow(self.parent, f"Calc: {self.formula['name']}", 480, 420)
        tk.Label(
            w.body, text=self.formula["expr"],
            font=("Consolas", 14, "bold"),
            bg="#c0c0c0", fg="#000080"
        ).pack(pady=8)
        tk.Label(
            w.body, text="Введите значения переменных:",
            bg="#c0c0c0", font=("Arial", 10)
        ).pack(anchor="w", padx=10)

        entries = {}
        rows = tk.Frame(w.body)
        rows.pack(fill="x", padx=10, pady=6)
        for var, desc in self.formula["vars"].items():
            row = tk.Frame(rows, bg="#c0c0c0")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{var} — {desc}", bg="#c0c0c0", width=32, anchor="w").pack(side="left")
            e = tk.Entry(row, width=12, font=("Consolas", 11))
            e.pack(side="right")
            entries[var] = e

        result_var = tk.StringVar()
        tk.Label(
            w.body, textvariable=result_var,
            bg="#000000", fg="#00ff00",
            font=("Consolas", 14, "bold"), height=2
        ).pack(fill="x", padx=10, pady=10)

        def compute():
            values = {}
            for var, e in entries.items():
                txt = e.get().strip().replace(",", ".")
                if not txt:
                    messagebox.showwarning("PyOS", f"Введите значение {var}")
                    return
                try:
                    values[var] = float(txt)
                except ValueError:
                    messagebox.showerror("PyOS", f"Некорректное значение {var}")
                    return
            result, err = self.solver.evaluate(self.formula["formula"], values)
            if err:
                result_var.set(f"Ошибка: {err}")
                return
            unit = self.formula.get("unit", "")
            result_var.set(f"{self.formula['solve']} = {result:.6g} {unit}".strip())

        tk.Button(
            w.body, text="Вычислить", font=("Arial", 11, "bold"),
            bg="#008000", fg="white", width=20, command=compute
        ).pack(pady=4)
        tk.Button(
            w.body, text="Сброс",
            bg="#c0c0c0", width=20,
            command=lambda: [e.delete(0, "end") for e in entries.values()] or result_var.set("")
        ).pack(pady=2)