import tkinter as tk
from tkinter import filedialog, messagebox
from gui.window import PyWindow


class Notepad:
    def __init__(self, parent, vfs):
        self.parent = parent
        self.vfs = vfs

    def run(self):
        w = PyWindow(self.parent, "Untitled - Notepad", 600, 400)
        text = tk.Text(w.body, wrap="word", font=("Consolas", 11), undo=True)
        text.pack(fill="both", expand=True)

        def save():
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text.get("1.0", "end-1c"))
                w.win.title(path.split("/")[-1] + " - Notepad")

        def open_file():
            path = filedialog.askopenfilename()
            if path:
                with open(path, "r", encoding="utf-8") as f:
                    text.delete("1.0", "end")
                    text.insert("1.0", f.read())
                w.win.title(path.split("/")[-1] + " - Notepad")

        menubar = tk.Menu(w.win)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=lambda: text.delete("1.0", "end"))
        filemenu.add_command(label="Open...", command=open_file)
        filemenu.add_command(label="Save...", command=save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=w.win.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        w.win.config(menu=menubar)