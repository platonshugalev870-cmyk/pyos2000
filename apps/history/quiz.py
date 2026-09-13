import tkinter as tk
from tkinter import messagebox
from gui.window import PyWindow
from apps.history.data import QUIZ_QUESTIONS
import random


class HistoryQuiz:
    def __init__(self, parent):
        self.parent = parent
        self.questions = []
        self.index = 0
        self.score = 0
        self.answered = False

    def run(self):
        self.win = PyWindow(self.parent, "History Quiz — PyOS 2000", 640, 480)
        self.questions = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS))

        header = tk.Frame(self.win.body, bg="#000080", height=36)
        header.pack(fill="x")
        header.pack_propagate(False)
        self.header_label = tk.Label(
            header, text="Историческая викторина",
            bg="#000080", fg="white", font=("Arial", 12, "bold")
        )
        self.header_label.pack(side="left", padx=10)

        self.score_label = tk.Label(
            self.win.body, text="Счёт: 0 / 0",
            bg="#c0c0c0", font=("Arial", 10, "bold"), anchor="e"
        )
        self.score_label.pack(fill="x", padx=10, pady=(6, 0))

        self.q_label = tk.Label(
            self.win.body, text="",
            bg="#c0c0c0", font=("Arial", 13, "bold"),
            wraplength=600, justify="left", anchor="w"
        )
        self.q_label.pack(fill="x", padx=10, pady=10)

        self.option_vars = []
        self.option_buttons = []
        options_frame = tk.Frame(self.win.body, bg="#c0c0c0")
        options_frame.pack(fill="x", padx=10, pady=4)
        for i in range(4):
            v = tk.StringVar()
            btn = tk.Radiobutton(
                options_frame, textvariable=v, value=str(i),
                bg="#c0c0c0", font=("Arial", 11),
                anchor="w", wraplength=580,
                activebackground="#c0c0c0",
                selectcolor="#a0a0ff"
            )
            btn.pack(fill="x", pady=2)
            self.option_vars.append((v, btn))

        self.explain_label = tk.Label(
            self.win.body, text="",
            bg="#c0c0c0", font=("Arial", 10, "italic"),
            fg="#000080", wraplength=600, justify="left", anchor="w"
        )
        self.explain_label.pack(fill="x", padx=10, pady=6)

        self.next_btn = tk.Button(
            self.win.body, text="Ответить",
            bg="#008000", fg="white", font=("Arial", 11, "bold"),
            width=18, command=self.on_next
        )
        self.next_btn.pack(pady=8)

        self.show_question()

    def show_question(self):
        self.answered = False
        self.explain_label.config(text="")
        self.next_btn.config(text="Ответить", bg="#008000")
        q = self.questions[self.index]
        self.q_label.config(text=f"Вопрос {self.index + 1} из {len(self.questions)}:\n\n{q['q']}")
        for (v, btn), text in zip(self.option_vars, q["options"]):
            v.set("")
            btn.config(text=text, state="normal")
        self.score_label.config(text=f"Счёт: {self.score} / {self.index}")

    def on_next(self):
        q = self.questions[self.index]
        if not self.answered:
            selected = None
            for i, (v, btn) in enumerate(self.option_vars):
                if v.get() == str(i):
                    selected = i
                    break
            if selected is None:
                messagebox.showwarning("PyOS", "Выберите вариант ответа.")
                return
            self.answered = True
            if selected == q["answer"]:
                self.score += 1
                self.explain_label.config(text="✓ Верно! " + q["explain"], fg="#006000")
            else:
                correct = q["answer"]
                self.explain_label.config(
                    text=f"✗ Неверно. Правильный ответ: {q['options'][correct]}\n{q['explain']}",
                    fg="#800000"
                )
            for i, (v, btn) in enumerate(self.option_vars):
                btn.config(state="disabled")
                if i == q["answer"]:
                    btn.config(fg="#006000")
                elif v.get() == str(i):
                    btn.config(fg="#800000")
            self.score_label.config(text=f"Счёт: {self.score} / {self.index + 1}")
            self.next_btn.config(text="Далее >")
            return
        self.index += 1
        if self.index >= len(self.questions):
            self.finish()
            return
        self.show_question()

    def finish(self):
        total = len(self.questions)
        pct = int(self.score / total * 100)
        msg = f"Викторина завершена!\n\nПравильных ответов: {self.score} из {total}\nРезультат: {pct}%"
        if pct >= 80:
            msg += "\n\nОтлично! Вы знаете историю."
        elif pct >= 50:
            msg += "\n\nХороший результат."
        else:
            msg += "\n\nСтоит повторить материал."
        messagebox.showinfo("History Quiz", msg)
        self.win.win.destroy()