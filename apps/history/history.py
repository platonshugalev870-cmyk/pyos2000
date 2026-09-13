import tkinter as tk
from tkinter import ttk
from gui.window import PyWindow
from apps.history import data
from apps.history.quiz import HistoryQuiz
from utils.animate import (
    gui_type_rich, fade_widget, pulse_text,
    animate_progress, wave_labels
)


TAGS = {
    "title": {"foreground": "#5a3a1a", "font": ("Arial", 16, "bold")},
    "rule": {"foreground": "#a08060"},
    "h2": {"foreground": "#8b0000", "font": ("Arial", 12, "bold")},
    "text": {"foreground": "#000000", "font": ("Consolas", 10)},
    "bullet": {"foreground": "#5a3a1a", "font": ("Consolas", 10, "bold")},
    "highlight": {"foreground": "#b06000", "font": ("Consolas", 10, "bold")},
    "dim": {"foreground": "#606060", "font": ("Consolas", 9, "italic")},
    "checkmark": {"foreground": "#8b5a2b", "font": ("Arial", 12, "bold")},
    "year": {"foreground": "#8b0000", "font": ("Consolas", 10, "bold")},
}


ERA_COLORS = {
    "Древний мир": "#8b5a2b",
    "Средние века": "#4a4a8b",
    "Новое время": "#2b6b2b",
    "Новейшее время": "#8b2b2b",
}


class HistoryApp:
    def __init__(self, parent):
        self.parent = parent
        self.data = data
        self.typing_state = None
        self.timeline_events = []

    def run(self):
        self.win = PyWindow(self.parent, "History Archive — PyOS 2000", 980, 680)
        self.win.win.geometry("980x680")

        top = tk.Frame(self.win.body, bg="#5a3a1a", height=48)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(
            top, text="  📜  History Archive",
            bg="#5a3a1a", fg="#f0d090",
            font=("Arial", 16, "bold")
        ).pack(side="left")
        self.status_label = tk.Label(
            top, text="Готов",
            bg="#5a3a1a", fg="#ffd080",
            font=("Arial", 10, "italic")
        )
        self.status_label.pack(side="right", padx=12)

        nb = ttk.Notebook(self.win.body)
        nb.pack(fill="both", expand=True, padx=6, pady=6)

        self.tab_eras = tk.Frame(nb, bg="#c0c0c0")
        self.tab_timeline = tk.Frame(nb, bg="#c0c0c0")
        self.tab_people = tk.Frame(nb, bg="#c0c0c0")
        self.tab_search = tk.Frame(nb, bg="#c0c0c0")
        self.tab_quiz = tk.Frame(nb, bg="#c0c0c0")

        nb.add(self.tab_eras, text="  Эпохи  ")
        nb.add(self.tab_timeline, text="  Хронология  ")
        nb.add(self.tab_people, text="  Личности  ")
        nb.add(self.tab_search, text="  Поиск  ")
        nb.add(self.tab_quiz, text="  Викторина  ")

        self.build_eras()
        self.build_timeline()
        self.build_people()
        self.build_search()
        self.build_quiz()

        nb.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.nb = nb

    def on_tab_change(self, event):
        tab = self.nb.tab(self.nb.select(), "text").strip()
        if tab == "Хронология" and not self.timeline_events:
            self.animate_timeline()

    # ---------- ЭПОХИ ----------

    def build_eras(self):
        left = tk.Frame(self.tab_eras, bg="#c0c0c0", width=230)
        left.pack(side="left", fill="y", padx=(6, 0), pady=6)
        left.pack_propagate(False)
        tk.Label(
            left, text="Исторические эпохи", bg="#c0c0c0",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 6))

        self.era_buttons = []
        for e in self.data.ERAS:
            lbl = tk.Label(
                left, text="  " + e["name"], bg="#c0c0c0",
                fg="#000000", font=("Arial", 10, "bold"), anchor="w",
                cursor="hand2", padx=6, pady=6
            )
            lbl.pack(fill="x", pady=1)
            color = ERA_COLORS.get(e["name"], "#000080")
            lbl.bind("<Button-1>", lambda ev, idx=len(self.era_buttons), c=color: self.select_era(idx, c))
            lbl.bind("<Enter>", lambda ev, w=lbl, c=color: w.config(bg=c, fg="white") if w.cget("fg") != "white" else None)
            lbl.bind("<Leave>", lambda ev, w=lbl: (w.config(bg="#c0c0c0", fg="#000000")) if w.cget("fg") != "white" or w.cget("bg") != ERA_COLORS.get(e["name"], "#000080") else None)
            self.era_buttons.append(lbl)

        right = tk.Frame(self.tab_eras, bg="#c0c0c0")
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        toolbar = tk.Frame(right, bg="#c0c0c0")
        toolbar.pack(fill="x")
        tk.Label(
            toolbar, text="Конспект эпохи", bg="#c0c0c0",
            font=("Arial", 11, "bold")
        ).pack(side="left")
        tk.Button(
            toolbar, text="↻ Повторить анимацию",
            bg="#5a3a1a", fg="white", font=("Arial", 9),
            command=self.replay_era
        ).pack(side="right")

        self.era_period = tk.Label(
            right, text="", bg="#c0c0c0", fg="#5a3a1a",
            font=("Arial", 11, "bold italic"), anchor="w"
        )
        self.era_period.pack(fill="x", pady=(4, 0))

        self.era_summary = tk.Text(
            right, wrap="word", bg="#fff8e0", fg="#000000",
            font=("Consolas", 10), relief="sunken", bd=2,
            padx=10, pady=8, cursor="arrow"
        )
        self.era_summary.pack(fill="both", expand=True, pady=(4, 0))
        for tag, cfg in TAGS.items():
            self.era_summary.tag_configure(tag, **cfg)

        self.current_era = 0
        self.select_era(0, ERA_COLORS.get(self.data.ERAS[0]["name"], "#5a3a1a"))

    def select_era(self, idx, color):
        for i, lbl in enumerate(self.era_buttons):
            if i == idx:
                lbl.config(bg=color, fg="white")
            else:
                lbl.config(bg="#c0c0c0", fg="#000000")
        self.current_era = idx
        self.animate_era(idx)

    def replay_era(self):
        self.animate_era(self.current_era)

    def animate_era(self, idx):
        if self.typing_state and self.typing_state.get("after"):
            try:
                self.era_summary.after_cancel(self.typing_state["after"])
            except tk.TclError:
                pass
        self.era_summary.delete("1.0", "end")
        e = self.data.ERAS[idx]
        self.set_status(f"Загрузка эпохи: {e['name']}...")
        segs = self.build_era_segments(e)

        def on_done():
            self.set_status(f"Эпоха загружена: {e['name']}")
            pulse_text(self.era_summary, "title", "#5a3a1a", "#c08040", steps=4, delay=100)

        self.typing_state = gui_type_rich(self.era_summary, segs, delay=4, callback=on_done)

    def build_era_segments(self, e):
        segs = []
        segs.append({"text": "  " + e["name"].upper() + "\n", "tags": ("title",), "delay": 14})
        segs.append({"text": "  " + "━" * (len(e["name"]) + 2) + "\n", "tags": ("rule",), "delay": 3})
        segs.append({"text": "  ", "tags": ("dim",), "delay": 8})
        segs.append({"text": "▌", "tags": ("checkmark",), "delay": 120})
        segs.append({"text": "Период: ", "tags": ("h2",), "delay": 15})
        segs.append({"text": f"{e['period']}\n\n", "tags": ("highlight",), "delay": 8})

        for line in e["summary"].split("\n"):
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
            else:
                segs.append({"text": line + "\n", "tags": ("text",), "delay": 4})

        segs.append({"text": "\n", "tags": (), "delay": 10})
        segs.append({"text": "  ", "tags": ("dim",), "delay": 8})
        segs.append({"text": "▌", "tags": ("checkmark",), "delay": 120})
        segs.append({"text": "Ключевых событий: ", "tags": ("h2",), "delay": 15})
        segs.append({"text": f"{len(e['events'])}\n", "tags": ("highlight",), "delay": 8})
        segs.append({"text": "  ", "tags": ("dim",), "delay": 8})
        segs.append({"text": "▌", "tags": ("checkmark",), "delay": 120})
        segs.append({"text": "Исторических личностей: ", "tags": ("h2",), "delay": 15})
        segs.append({"text": f"{len(e['people'])}\n", "tags": ("highlight",), "delay": 8})
        segs.append({"text": "\n", "tags": (), "delay": 10})
        segs.append({"text": "  ", "tags": (), "delay": 5})
        segs.append({"text": "━" * 42 + "\n", "tags": ("rule",), "delay": 4})
        return segs

    # ---------- ХРОНОЛОГИЯ (анимированная) ----------

    def build_timeline(self):
        tk.Label(
            self.tab_timeline, text="Глобальная хронология событий",
            bg="#c0c0c0", font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 0))

        legend = tk.Frame(self.tab_timeline, bg="#c0c0c0")
        legend.pack(fill="x", padx=10, pady=4)
        self.legend_labels = []
        for era, color in ERA_COLORS.items():
            dot = tk.Label(legend, text=" ● ", fg=color, bg="#c0c0c0", font=("Arial", 14, "bold"))
            dot.pack(side="left")
            lbl = tk.Label(legend, text=era, bg="#c0c0c0", font=("Arial", 9))
            lbl.pack(side="left", padx=(0, 12))
            self.legend_labels.append(lbl)

        tl_container = tk.Frame(self.tab_timeline, bg="#c0c0c0")
        tl_container.pack(fill="x", padx=10)
        self.timeline_canvas = tk.Canvas(
            tl_container, bg="#1a1a2e", height=160, highlightthickness=0
        )
        self.timeline_canvas.pack(fill="x")
        self.timeline_canvas.bind("<Configure>", lambda e: self.draw_timeline())
        self.timeline_canvas.bind("<Motion>", self.on_timeline_motion)
        self.timeline_canvas.bind("<Leave>", lambda e: self.timeline_tooltip.place_forget())
        self.timeline_tooltip = tk.Label(
            self.tab_timeline, text="", bg="#ffffe0", fg="#000000",
            font=("Arial", 9), relief="solid", bd=1
        )

        prog_frame = tk.Frame(self.tab_timeline, bg="#c0c0c0")
        prog_frame.pack(fill="x", padx=10, pady=(4, 0))
        self.timeline_progress = tk.Label(
            prog_frame, text="", bg="#c0c0c0", fg="#5a3a1a",
            font=("Consolas", 14, "bold"), anchor="w"
        )
        self.timeline_progress.pack(fill="x")

        tk.Label(
            self.tab_timeline, text="Все события (по возрастанию даты)",
            bg="#c0c0c0", font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 4))

        cols = tk.Frame(self.tab_timeline, bg="#c0c0c0")
        cols.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.timeline_tree = ttk.Treeview(
            cols, columns=("year", "title", "era"),
            show="headings", height=10
        )
        self.timeline_tree.heading("year", text="Дата")
        self.timeline_tree.heading("title", text="Событие")
        self.timeline_tree.heading("era", text="Эпоха")
        self.timeline_tree.column("year", width=130, anchor="center")
        self.timeline_tree.column("title", width=420)
        self.timeline_tree.column("era", width=200)
        self.timeline_tree.pack(fill="both", expand=True)
        for era, color in ERA_COLORS.items():
            self.timeline_tree.tag_configure(era, foreground=color)

    def animate_timeline(self):
        self.timeline_events = []
        events = sorted(self.data.TIMELINE_GLOBAL, key=lambda x: x["year"])
        self.set_status("Построение хронологии...")
        wave_labels(self.legend_labels, "#c0c0c0", "#ffe080", per_step=80)

        def add_event(i):
            if i >= len(events):
                self.set_status("Хронология построена")
                return
            e = events[i]
            self.timeline_events.append(e)
            self.draw_timeline()
            self.timeline_tree.insert(
                "", "end",
                values=(e["label"], e["title"], e["era"]),
                tags=(e["era"],)
            )
            self.timeline_tree.see(self.timeline_tree.get_children()[-1])
            self.update_progress_bar(i + 1, len(events))
            self.win.win.after(90, lambda: add_event(i + 1))

        def start():
            add_event(0)

        self.win.win.after(200, start)

    def update_progress_bar(self, current, total):
        filled = int(30 * current / total)
        bar = "█" * filled + "░" * (30 - filled)
        self.timeline_progress.config(
            text=f"  [{bar}] {current}/{total}"
        )

    def draw_timeline(self):
        c = self.timeline_canvas
        c.delete("all")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 10 or not self.timeline_events:
            return
        years = [e["year"] for e in self.timeline_events]
        ymin, ymax = min(years), max(years)
        span = ymax - ymin or 1
        margin = 45
        usable = w - 2 * margin
        line_y = h // 2 + 15
        c.create_line(margin, line_y, w - margin, line_y, fill="#707080", width=3)
        for i in range(0, 11):
            x = margin + usable * i / 10
            c.create_line(x, line_y - 4, x, line_y + 4, fill="#505060")
        self.positions = []
        for e in self.timeline_events:
            x = margin + usable * (e["year"] - ymin) / span
            color = ERA_COLORS.get(e["era"], "#ffffff")
            c.create_oval(x - 7, line_y - 7, x + 7, line_y + 7, fill=color, outline="#ffffff", width=1)
            c.create_text(
                x, line_y + 20, text=e["label"],
                fill="#c0c0d0", font=("Arial", 7)
            )
            self.positions.append((x, line_y, e))

    def on_timeline_motion(self, event):
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
            self.timeline_tooltip.config(text=text)
            self.timeline_tooltip.place(x=x - 80, y=y - 50)
        else:
            self.timeline_tooltip.place_forget()

    # ---------- ЛИЧНОСТИ ----------

    def build_people(self):
        top = tk.Frame(self.tab_people, bg="#c0c0c0")
        top.pack(fill="x", padx=10, pady=8)
        tk.Label(top, text="Эпоха:", bg="#c0c0c0", font=("Arial", 10, "bold")).pack(side="left")
        self.people_filter = ttk.Combobox(
            top, values=["Все эпохи"] + [e["name"] for e in self.data.ERAS],
            state="readonly", width=25
        )
        self.people_filter.current(0)
        self.people_filter.pack(side="left", padx=8)
        self.people_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_people())

        cols = tk.Frame(self.tab_people, bg="#c0c0c0")
        cols.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.people_tree = ttk.Treeview(
            cols, columns=("era", "name", "years", "role"),
            show="headings"
        )
        self.people_tree.heading("era", text="Эпоха")
        self.people_tree.heading("name", text="Имя")
        self.people_tree.heading("years", text="Годы")
        self.people_tree.heading("role", text="Роль")
        self.people_tree.column("era", width=150)
        self.people_tree.column("name", width=190)
        self.people_tree.column("years", width=150)
        self.people_tree.column("role", width=400)
        self.people_tree.pack(fill="both", expand=True)
        for era, color in ERA_COLORS.items():
            self.people_tree.tag_configure(era, foreground=color)
        self.refresh_people(animate=True)

    def refresh_people(self, animate=False):
        for i in self.people_tree.get_children():
            self.people_tree.delete(i)
        sel = self.people_filter.get()
        rows = []
        for e in self.data.ERAS:
            if sel != "Все эпохи" and e["name"] != sel:
                continue
            for p in e["people"]:
                rows.append((e["name"], p["name"], p["years"], p["role"]))
        if not animate:
            for r in rows:
                self.people_tree.insert("", "end", values=r, tags=(r[0],))
            return
        self.set_status("Загрузка личностей...")

        def add(i):
            if i >= len(rows):
                self.set_status("Личности загружены")
                return
            r = rows[i]
            self.people_tree.insert("", "end", values=r, tags=(r[0],))
            self.people_tree.see(self.people_tree.get_children()[-1])
            self.win.win.after(45, lambda: add(i + 1))

        add(0)

    # ---------- ПОИСК ----------

    def build_search(self):
        top = tk.Frame(self.tab_search, bg="#c0c0c0")
        top.pack(fill="x", padx=10, pady=10)
        tk.Label(
            top, text="Поиск по событиям и личностям:",
            bg="#c0c0c0", font=("Arial", 11, "bold")
        ).pack(side="left")
        self.search_entry = tk.Entry(top, font=("Consolas", 12), width=40)
        self.search_entry.pack(side="left", padx=8)
        self.search_entry.bind("<Return>", lambda e: self.do_search())
        tk.Button(top, text="Найти", bg="#5a3a1a", fg="white", width=10, command=self.do_search).pack(side="left")

        self.search_results = tk.Text(
            self.tab_search, bg="#fff8e0", font=("Consolas", 10),
            relief="sunken", bd=2, padx=10, pady=8
        )
        self.search_results.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.search_results.tag_configure("header", foreground="#5a3a1a", font=("Arial", 11, "bold"))
        self.search_results.tag_configure("year", foreground="#8b0000", font=("Consolas", 11, "bold"))
        self.search_results.tag_configure("title", foreground="#000000", font=("Consolas", 11, "bold"))
        self.search_results.tag_configure("desc", foreground="#404040", font=("Consolas", 10))
        self.search_results.tag_configure("dim", foreground="#808080", font=("Consolas", 9, "italic"))

    def do_search(self):
        q = self.search_entry.get().strip().lower()
        self.search_results.delete("1.0", "end")
        if not q:
            return
        segs = []
        found = 0
        for era in self.data.ERAS:
            for e in era["events"]:
                if q in e["title"].lower() or q in e["desc"].lower():
                    segs.append({"text": f"▌ [{era['name']}]  ", "tags": ("dim",), "delay": 3})
                    segs.append({"text": f"{e['year_label']}\n", "tags": ("year",), "delay": 6})
                    segs.append({"text": f"  {e['title']}\n", "tags": ("title",), "delay": 4})
                    segs.append({"text": f"  {e['desc']}\n\n", "tags": ("desc",), "delay": 2})
                    found += 1
            for p in era["people"]:
                if q in p["name"].lower() or q in p["role"].lower():
                    segs.append({"text": f"▌ [{era['name']}] Личность\n", "tags": ("dim",), "delay": 3})
                    segs.append({"text": f"  {p['name']} ({p['years']})\n", "tags": ("title",), "delay": 6})
                    segs.append({"text": f"  {p['role']}\n\n", "tags": ("desc",), "delay": 2})
                    found += 1
        if found == 0:
            self.search_results.insert("end", "Ничего не найдено.\n", "dim")
            return
        segs.append({"text": f"Всего найдено: {found}\n", "tags": ("header",), "delay": 6})
        gui_type_rich(self.search_results, segs, delay=5)

    # ---------- ВИКТОРИНА ----------

    def build_quiz(self):
        frame = tk.Frame(self.tab_quiz, bg="#c0c0c0")
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        self.quiz_title = tk.Label(
            frame, text="📜 Историческая викторина",
            bg="#c0c0c0", font=("Arial", 18, "bold"), fg="#5a3a1a"
        )
        self.quiz_title.pack(pady=(20, 10))
        info = (
            "Проверьте свои знания истории!\n\n"
            f"• {len(self.data.QUIZ_QUESTIONS)} вопросов с вариантами ответов\n"
            "• Мгновенная проверка и пояснение\n"
            "• Итоговая оценка в процентах\n\n"
            "Вопросы выбираются в случайном порядке."
        )
        self.quiz_info = tk.Label(
            frame, text="", bg="#c0c0c0", font=("Arial", 11), justify="left"
        )
        self.quiz_info.pack(pady=10)
        tk.Button(
            frame, text="▶  Начать викторину",
            font=("Arial", 13, "bold"), bg="#5a3a1a", fg="#f0d090",
            width=22, height=2,
            command=self.start_quiz
        ).pack(pady=20)
        segs = [{"text": line + "\n", "tags": (), "delay": 6} for line in info.split("\n")]
        self.win.win.after(400, lambda: gui_type_rich(self.quiz_info, segs, delay=8))

    def start_quiz(self):
        HistoryQuiz(self.parent).run()

    # ---------- ВСПОМОГАТЕЛЬНОЕ ----------

    def set_status(self, text):
        self.status_label.config(text=text)