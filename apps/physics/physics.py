import tkinter as tk
from tkinter import ttk
from gui.window import PyWindow
from apps.physics import data
from apps.physics.solver import Solver
from apps.physics.calculator import FormulaCalculator
from utils.animate import gui_type_rich, gui_type_lines


TAGS = {
    "title": {"foreground": "#000080", "font": ("Arial", 16, "bold")},
    "rule": {"foreground": "#808080"},
    "h2": {"foreground": "#8b0000", "font": ("Arial", 12, "bold")},
    "text": {"foreground": "#000000", "font": ("Consolas", 10)},
    "formula": {"foreground": "#006000", "font": ("Consolas", 11, "bold")},
    "bullet": {"foreground": "#000080", "font": ("Consolas", 10)},
    "highlight": {"foreground": "#ff0000", "font": ("Consolas", 10, "bold")},
    "dim": {"foreground": "#606060", "font": ("Consolas", 9, "italic")},
    "checkmark": {"foreground": "#009000", "font": ("Arial", 12, "bold")},
}


class PhysicsApp:
    def __init__(self, parent):
        self.parent = parent
        self.data = data
        self.solver = Solver(data)
        self.typing_state = None
        self.current_section = 0
        self.current_formula = None
        self.visible_formulas = []

    def run(self):
        self.win = PyWindow(self.parent, "Physics Lab — PyOS 2000", 960, 660)
        self.win.win.geometry("960x660")
        top = tk.Frame(self.win.body, bg="#000080", height=48)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(
            top, text="  ⚛  Physics Lab",
            bg="#000080", fg="white",
            font=("Arial", 16, "bold")
        ).pack(side="left")
        self.status_label = tk.Label(
            top, text="Готов",
            bg="#000080", fg="#80ff80",
            font=("Arial", 10, "italic")
        )
        self.status_label.pack(side="right", padx=12)
        nb = ttk.Notebook(self.win.body)
        nb.pack(fill="both", expand=True, padx=6, pady=6)
        self.nb = nb
        self.tab_sections = tk.Frame(nb, bg="#c0c0c0")
        self.tab_formulas = tk.Frame(nb, bg="#c0c0c0")
        self.tab_search = tk.Frame(nb, bg="#c0c0c0")
        self.tab_const = tk.Frame(nb, bg="#c0c0c0")
        self.tab_solver = tk.Frame(nb, bg="#c0c0c0")
        nb.add(self.tab_sections, text="  Конспекты  ")
        nb.add(self.tab_formulas, text="  Формулы  ")
        nb.add(self.tab_search, text="  Поиск  ")
        nb.add(self.tab_const, text="  Константы  ")
        nb.add(self.tab_solver, text="  Решатель задач  ")
        self.build_sections()
        self.build_formulas()
        self.build_search()
        self.build_constants()
        self.build_solver()


    def build_sections(self):
        left = tk.Frame(self.tab_sections, bg="#c0c0c0", width=230)
        left.pack(side="left", fill="y", padx=(6, 0), pady=6)
        left.pack_propagate(False)
        tk.Label(
            left, text="Разделы физики", bg="#c0c0c0",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 6))
        self.section_buttons = []
        for s in self.data.SECTIONS:
            lbl = tk.Label(
                left, text="  " + s["name"], bg="#c0c0c0",
                fg="#000000", font=("Arial", 10), anchor="w",
                cursor="hand2", padx=6, pady=3
            )
            lbl.pack(fill="x", pady=1)
            idx = len(self.section_buttons)
            lbl.bind("<Button-1>", lambda e, i=idx: self.select_section(i))
            lbl.bind("<Enter>", lambda e, w=lbl: self._hover_in(w))
            lbl.bind("<Leave>", lambda e, w=lbl: self._hover_out(w))
            self.section_buttons.append(lbl)
        right = tk.Frame(self.tab_sections, bg="#c0c0c0")
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        toolbar = tk.Frame(right, bg="#c0c0c0")
        toolbar.pack(fill="x")
        tk.Label(
            toolbar, text="Конспект", bg="#c0c0c0",
            font=("Arial", 11, "bold")
        ).pack(side="left")
        tk.Button(
            toolbar, text="↻ Повторить анимацию",
            bg="#000080", fg="white", font=("Arial", 9),
            command=self.replay_section_animation
        ).pack(side="right")
        self.summary = tk.Text(
            right, wrap="word", bg="#ffffff", fg="#000000",
            font=("Consolas", 10), relief="sunken", bd=2,
            padx=10, pady=8, cursor="arrow"
        )
        self.summary.pack(fill="both", expand=True, pady=(6, 0))
        for tag, cfg in TAGS.items():
            self.summary.tag_configure(tag, **cfg)
        self.select_section(0)

    def _hover_in(self, widget):
        if widget.cget("bg") != "#000080":
            widget.config(bg="#a0a0ff")

    def _hover_out(self, widget):
        if widget.cget("bg") != "#000080":
            widget.config(bg="#c0c0c0")

    def select_section(self, idx):
        for i, lbl in enumerate(self.section_buttons):
            if i == idx:
                lbl.config(bg="#000080", fg="white")
            else:
                lbl.config(bg="#c0c0c0", fg="#000000")
        self.current_section = idx
        self.animate_section(idx)

    def replay_section_animation(self):
        self.animate_section(self.current_section)

    def animate_section(self, idx):
        if self.typing_state and self.typing_state.get("after"):
            try:
                self.summary.after_cancel(self.typing_state["after"])
            except tk.TclError:
                pass
        self.summary.delete("1.0", "end")
        s = self.data.SECTIONS[idx]
        self.set_status(f"Загрузка конспекта: {s['name']}...")
        segments = self.build_section_segments(s)

        def on_done():
            self.set_status(f"Конспект загружен: {s['name']}")
        self.typing_state = gui_type_rich(
            self.summary, segments, delay=4, callback=on_done
        )

    def build_section_segments(self, s):
        segs = []
        segs.append({"text": "  " + s["name"].upper() + "\n", "tags": ("title",), "delay": 12})
        segs.append({"text": "  " + "━" * (len(s["name"]) + 2) + "\n\n", "tags": ("rule",), "delay": 3})
        segs.append({"text": "  ", "tags": ("dim",), "delay": 8})
        segs.append({"text": "▌", "tags": ("checkmark",), "delay": 120})
        segs.append({"text": "Конспект\n", "tags": ("h2",), "delay": 25})
        segs.append({"text": "\n", "tags": (), "delay": 10})
        for line in s["summary"].split("\n"):
            stripped = line.lstrip()
            if not stripped:
                segs.append({"text": "\n", "tags": (), "delay": 30})
                continue
            if stripped.startswith("•"):
                segs.append({"text": "    ", "tags": (), "delay": 1})
                segs.append({"text": "● ", "tags": ("bullet",), "delay": 30})
                segs.append({"text": stripped[1:].strip() + "\n", "tags": ("text",), "delay": 5})
            elif stripped.startswith("  •"):
                segs.append({"text": "        ", "tags": (), "delay": 1})
                segs.append({"text": "◦ ", "tags": ("bullet",), "delay": 30})
                segs.append({"text": stripped[2:].strip() + "\n", "tags": ("text",), "delay": 5})
            elif "=" in line and any(
                x in line for x in
                ["p =", "F =", "U =", "A =", "E =", "v =", "S =", "T =", "R =", "I =", "h·", "m·"]
            ):
                segs.append({"text": "    " + line.strip() + "\n", "tags": ("formula",), "delay": 8})
            else:
                segs.append({"text": line + "\n", "tags": ("text",), "delay": 4})
        segs.append({"text": "\n", "tags": (), "delay": 10})
        segs.append({"text": "  ", "tags": ("dim",), "delay": 8})
        segs.append({"text": "▌", "tags": ("checkmark",), "delay": 120})
        segs.append({"text": "Раздел: ", "tags": ("h2",), "delay": 20})
        segs.append({"text": f"{s['name']}", "tags": ("highlight",), "delay": 10})
        segs.append({"text": f"    Формул: {len(s['formulas'])}\n", "tags": ("dim",), "delay": 4})
        segs.append({"text": "  ", "tags": (), "delay": 5})
        segs.append({"text": "━" * 40 + "\n", "tags": ("rule",), "delay": 4})
        return segs

    def build_formulas(self):
        left = tk.Frame(self.tab_formulas, bg="#c0c0c0", width=300)
        left.pack(side="left", fill="y", padx=(6, 0), pady=6)
        left.pack_propagate(False)
        tk.Label(
            left, text="Список формул", bg="#c0c0c0",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 4))
        self.section_filter = ttk.Combobox(
            left, values=["Все разделы"] + [s["name"] for s in self.data.SECTIONS],
            state="readonly"
        )
        self.section_filter.current(0)
        self.section_filter.pack(fill="x", pady=4)
        self.section_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_formulas())
        self.formula_list = tk.Listbox(
            left, font=("Consolas", 10), activestyle="none",
            selectbackground="#000080", selectforeground="white"
        )
        self.formula_list.pack(fill="both", expand=True)
        self.formula_list.bind("<<ListboxSelect>>", self.on_formula_select)
        right = tk.Frame(self.tab_formulas, bg="#c0c0c0")
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        tk.Label(
            right, text="Формула", bg="#c0c0c0",
            font=("Arial", 11, "bold")
        ).pack(anchor="w")
        self.formula_expr = tk.Label(
            right, text="", bg="#000000", fg="#00ff00",
            font=("Consolas", 20, "bold"), height=2, anchor="w"
        )
        self.formula_expr.pack(fill="x", pady=6)
        tk.Label(
            right, text="Переменные:", bg="#c0c0c0",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")
        self.formula_vars = tk.Text(
            right, height=10, bg="#ffffff", font=("Consolas", 10),
            relief="sunken", bd=2, padx=8, pady=6
        )
        self.formula_vars.pack(fill="x", pady=4)
        self.btn_calc = tk.Button(
            right, text="Открыть калькулятор",
            font=("Arial", 11, "bold"), bg="#008000", fg="white",
            state="disabled", command=self.open_formula_calculator
        )
        self.btn_calc.pack(pady=8)
        self.refresh_formulas()

    def refresh_formulas(self):
        self.formula_list.delete(0, "end")
        sel = self.section_filter.get()
        self.visible_formulas = []
        for s in self.data.SECTIONS:
            if sel != "Все разделы" and s["name"] != sel:
                continue
            for f in s["formulas"]:
                self.visible_formulas.append(f)
                self.formula_list.insert("end", f"  {f['name']}")

    def on_formula_select(self, event=None):
        idx = self.formula_list.curselection()
        if not idx or idx[0] >= len(self.visible_formulas):
            return
        f = self.visible_formulas[idx[0]]
        self.current_formula = f
        self.formula_expr.config(text="")
        self.formula_vars.delete("1.0", "end")
        expr_text = "  " + f["expr"]
        state = {"i": 0}

        def var_lines():
            self.formula_vars.tag_configure("name", foreground="#000080", font=("Consolas", 10, "bold"))
            self.formula_vars.tag_configure("desc", foreground="#000000", font=("Consolas", 10))
            self.formula_vars.tag_configure("solve", foreground="#c00000", font=("Consolas", 11, "bold"))
            segs = []
            for var, desc in f["vars"].items():
                segs.append({"text": f"  {var:<10}", "tags": ("name",), "delay": 6})
                segs.append({"text": f" — {desc}\n", "tags": ("desc",), "delay": 3})
            segs.append({"text": "\n", "tags": (), "delay": 5})
            segs.append({"text": "  Ищем:  ", "tags": ("solve",), "delay": 8})
            segs.append({"text": f"{f['solve']}  [{f.get('unit', '')}]\n", "tags": ("solve",), "delay": 8})
            gui_type_rich(self.formula_vars, segs, delay=6)
            self.btn_calc.config(state="normal")

        def step():
            if state["i"] >= len(expr_text):
                self._pulse_bg(self.formula_expr, "#000000", "#003300", 6, 90)
                var_lines()
                return
            self.formula_expr.config(text=self.formula_expr.cget("text") + expr_text[state["i"]])
            state["i"] += 1
            self.formula_expr.after(25, step)
        step()

    def _pulse_bg(self, widget, color_a, color_b, steps=6, delay=80):
        def step(i):
            if i > steps:
                try:
                    widget.config(bg=color_a)
                except tk.TclError:
                    pass
                return
            try:
                widget.config(bg=color_b if i % 2 == 0 else color_a)
            except tk.TclError:
                return
            widget.after(delay, lambda: step(i + 1))
        step(0)

    def open_formula_calculator(self):
        if not self.current_formula:
            return
        FormulaCalculator(self.parent, self.current_formula, self.solver).run()

    def build_search(self):
        top = tk.Frame(self.tab_search, bg="#c0c0c0")
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(
            top, text="Поиск формулы:", bg="#c0c0c0",
            font=("Arial", 11, "bold")
        ).pack(side="left")
        self.search_entry = tk.Entry(top, font=("Consolas", 12), width=40)
        self.search_entry.pack(side="left", padx=8)
        self.search_entry.bind("<Return>", lambda e: self.do_search())
        tk.Button(
            top, text="Найти", command=self.do_search,
            bg="#000080", fg="white", width=10
        ).pack(side="left")

        self.search_results = tk.Text(
            self.tab_search, bg="#ffffff", font=("Consolas", 10),
            relief="sunken", bd=2, padx=10, pady=8
        )
        self.search_results.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.search_results.tag_configure("header", foreground="#000080", font=("Arial", 11, "bold"))
        self.search_results.tag_configure("expr", foreground="#006000", font=("Consolas", 11, "bold"))
        self.search_results.tag_configure("var", foreground="#000000", font=("Consolas", 10))
        self.search_results.tag_configure("dim", foreground="#808080", font=("Consolas", 9, "italic"))

    def do_search(self):
        query = self.search_entry.get().strip()
        self.search_results.delete("1.0", "end")
        if not query:
            return
        matches = self.solver.find_formula(query)
        if not matches:
            self.search_results.insert("end", "Ничего не найдено.\n", "dim")
            return
        segs = []
        segs.append({"text": f"Найдено совпадений: {len(matches)}\n\n", "tags": ("header",), "delay": 8})
        for section, f in matches:
            segs.append({"text": f"▌ [{section}]\n", "tags": ("dim",), "delay": 8})
            segs.append({"text": f"  {f['name']}\n", "tags": ("header",), "delay": 5})
            segs.append({"text": f"  {f['expr']}\n", "tags": ("expr",), "delay": 4})
            for var, desc in f["vars"].items():
                segs.append({"text": f"      {var:<10} — {desc}\n", "tags": ("var",), "delay": 2})
            segs.append({"text": "\n", "tags": (), "delay": 20})
        gui_type_rich(self.search_results, segs, delay=5)

    def build_constants(self):
        tk.Label(
            self.tab_const, text="Физические постоянные",
            bg="#c0c0c0", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=10)
        cols = tk.Frame(self.tab_const, bg="#c0c0c0")
        cols.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tree = ttk.Treeview(cols, columns=("sym", "name", "val", "unit"), show="headings")
        tree.heading("sym", text="Обозн.")
        tree.heading("name", text="Величина")
        tree.heading("val", text="Значение")
        tree.heading("unit", text="Ед.")
        tree.column("sym", width=90, anchor="center")
        tree.column("name", width=340)
        tree.column("val", width=170, anchor="e")
        tree.column("unit", width=100, anchor="center")
        tree.pack(fill="both", expand=True)
        tree.tag_configure("even", background="#e8e8ff")
        tree.tag_configure("odd", background="#ffffff")
        for i, (sym, c) in enumerate(self.data.CONSTANTS.items()):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert(
                "", "end",
                values=(sym, c["name"], f"{c['value']:.4g}", c["unit"]),
                tags=(tag,)
            )

    def build_solver(self):
        top = tk.Frame(self.tab_solver, bg="#c0c0c0")
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(
            top, text="Введите условие задачи:",
            bg="#c0c0c0", font=("Arial", 11, "bold")
        ).pack(anchor="w")
        tk.Label(
            top,
            text='Например: «найти кинетическую энергию тела массой 2 кг, движущегося со скоростью 5 м/с»',
            bg="#c0c0c0", font=("Arial", 9, "italic"), fg="#606060"
        ).pack(anchor="w", pady=(0, 4))
        self.task_entry = tk.Text(
            top, font=("Consolas", 11), height=3,
            bg="#ffffff", relief="sunken", bd=2, wrap="word"
        )
        self.task_entry.pack(fill="x", pady=4)
        btn_row = tk.Frame(top, bg="#c0c0c0")
        btn_row.pack(fill="x", pady=4)
        tk.Button(
            btn_row, text="▶  Решить", bg="#008000", fg="white",
            width=16, font=("Arial", 11, "bold"),
            command=self.solve_task
        ).pack(side="left")
        tk.Button(
            btn_row, text="Очистить", bg="#c0c0c0",
            width=12, command=self.clear_solver
        ).pack(side="left", padx=6)
        tk.Button(
            btn_row, text="Пример", bg="#000080", fg="white",
            width=12, command=self.load_example
        ).pack(side="left", padx=6)
        examples_frame = tk.Frame(self.tab_solver, bg="#c0c0c0")
        examples_frame.pack(fill="x", padx=10)
        tk.Label(
            examples_frame, text="Быстрые примеры:",
            bg="#c0c0c0", font=("Arial", 9, "bold")
        ).pack(anchor="w")
        row = tk.Frame(examples_frame, bg="#c0c0c0")
        row.pack(fill="x", pady=2)
        examples = [
            "найти кинетическую энергию тела массой 2 кг, движущегося со скоростью 5 м/с",
            "найти силу, если масса 3 кг, ускорение 4 м/с²",
            "найти работу, если сила 10 Н, путь 5 м",
            "найти силу тока, если напряжение 12 В, сопротивление 4 Ом",
            "найти период математического маятника длиной 1 м",
        ]
        for ex in examples:
            short = ex[:34] + "…" if len(ex) > 36 else ex
            tk.Button(
                row, text=short, font=("Arial", 8),
                bg="#e0e0e0", relief="groove",
                command=lambda t=ex: self.set_task(t)
            ).pack(side="left", padx=2)
        self.solver_log = tk.Text(
            self.tab_solver, bg="#0a0a0a", fg="#00ff00",
            font=("Consolas", 10), relief="sunken", bd=2,
            padx=10, pady=8, wrap="word"
        )
        self.solver_log.pack(fill="both", expand=True, padx=10, pady=(6, 10))
        self.solver_log.tag_configure("header", foreground="#ffff00", font=("Consolas", 12, "bold"))
        self.solver_log.tag_configure("step", foreground="#00ffff", font=("Consolas", 11, "bold"))
        self.solver_log.tag_configure("formula", foreground="#80ff80", font=("Consolas", 11, "bold"))
        self.solver_log.tag_configure("subst", foreground="#ffa0a0", font=("Consolas", 10))
        self.solver_log.tag_configure("answer", foreground="#ffffff", background="#006000", font=("Consolas", 13, "bold"))
        self.solver_log.tag_configure("dim", foreground="#808080", font=("Consolas", 9, "italic"))
        self.solver_log.tag_configure("error", foreground="#ff6060", font=("Consolas", 11, "bold"))
        self.solver_log.tag_configure("value", foreground="#ffd080", font=("Consolas", 10, "bold"))

    def set_task(self, text):
        self.task_entry.delete("1.0", "end")
        self.task_entry.insert("1.0", text)

    def clear_solver(self):
        self.task_entry.delete("1.0", "end")
        self.solver_log.delete("1.0", "end")

    def load_example(self):
        self.set_task("найти кинетическую энергию тела массой 2 кг, движущегося со скоростью 5 м/с")

    def solve_task(self):
        text = self.task_entry.get("1.0", "end").strip()
        self.solver_log.delete("1.0", "end")
        if not text:
            self.solver_log.insert("end", "Введите условие задачи.\n", "dim")
            return
        self.set_status("Решение задачи...")
        result = self.solver.solve_task(text)
        self.render_solution(result)

    def render_solution(self, result):
        log = self.solver_log
        parsed = result["parsed"]
        log.insert("end", "═" * 60 + "\n", "dim")
        log.insert("end", "  РЕШЕНИЕ ЗАДАЧИ\n", "header")
        log.insert("end", "═" * 60 + "\n\n", "dim")
        log.insert("end", "Условие: ", "dim")
        log.insert("end", parsed["text"] + "\n\n")
        if result["error"]:
            log.insert("end", "⚠  " + result["error"] + "\n\n", "error")
            if result["known"]:
                log.insert("end", "Распознанные величины:\n", "step")
                for k, v in result["known"].items():
                    log.insert("end", f"  {k} = {v:g}\n")
            if result["candidates"]:
                log.insert("end", "\nВозможные формулы:\n", "dim")
                for score, name, expr, missing in result["candidates"]:
                    log.insert("end", f"  • {name}: {expr}", "formula")
                    missing_str = ", ".join(missing) if missing else "—"
                    log.insert("end", f"   (не хватает: {missing_str})\n", "dim")
            self.set_status("Задача не решена")
            return
        log.insert("end", f"Распознано величин: {len(result['known'])}\n", "dim")
        for k, v in result["known"].items():
            log.insert("end", f"    {k} = ", "step")
            log.insert("end", f"{v:g}\n", "value")
        log.insert("end", "\n", "")
        for step in result["steps"]:
            t = step["type"]
            if t == "given":
                log.insert("end", "▌ Дано:\n", "step")
                for line in step["lines"]:
                    log.insert("end", line + "\n", "value")
                log.insert("end", "\n")
            elif t == "target":
                log.insert("end", "▌ Найти:\n", "step")
                for line in step["lines"]:
                    log.insert("end", line + "\n", "value")
                log.insert("end", "\n")
            elif t == "formula":
                log.insert("end", "▌ " + step["title"] + "\n", "step")
                for line in step["lines"]:
                    log.insert("end", line + "\n", "formula")
                log.insert("end", "\n")
            elif t == "subst":
                log.insert("end", "▌ Подстановка:\n", "dim")
                for line in step["lines"]:
                    log.insert("end", line + "\n", "subst")
                log.insert("end", "\n")
            elif t == "answer":
                log.insert("end", "═" * 60 + "\n", "dim")
                for line in step["lines"]:
                    log.insert("end", line + "\n", "answer")
                log.insert("end", "═" * 60 + "\n", "dim")
        ans = result["answer"]
        self.set_status(f"Ответ: {ans['target']} = {ans['value']:.6g} {ans['unit']}")

    def set_status(self, text):
        self.status_label.config(text=text)