import tkinter as tk
from tkinter import messagebox
from gui.window import PyWindow


class Explorer:
    def __init__(self, parent, vfs):
        self.parent = parent
        self.vfs = vfs
        self.cwd = "/"

    def run(self):
        w = PyWindow(self.parent, "My Computer", 620, 420)
        top = tk.Frame(w.body)
        top.pack(fill="x")
        path_label = tk.Label(top, text="/", anchor="w", bg="#c0c0c0")
        path_label.pack(side="left", fill="x", expand=True)

        listbox = tk.Listbox(w.body, font=("Consolas", 11))
        listbox.pack(fill="both", expand=True, pady=8)

        def refresh():
            listbox.delete(0, "end")
            path_label.config(text=self.cwd)
            items = sorted(self.vfs.ls(self.cwd))
            for i in items:
                full = self.cwd.rstrip("/") + "/" + i
                meta = self.vfs.meta.get(full, {})
                tag = "[DIR]" if meta.get("type") == "dir" else str(meta.get("size", 0)) + " B"
                listbox.insert("end", f"{tag:<10} {i}")
            return items

        def on_double(e):
            sel = listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            items = refresh()
            if idx >= len(items):
                return
            name = items[idx]
            full = self.cwd.rstrip("/") + "/" + name
            meta = self.vfs.meta.get(full, {})
            if meta.get("type") == "dir":
                self.cwd = full
                refresh()
            else:
                data = self.vfs.read(full)
                messagebox.showinfo(name, data[:2000] if data else "(empty)")

        def go_up():
            parts = [p for p in self.cwd.split("/") if p]
            self.cwd = "/" + "/".join(parts[:-1]) if parts[:-1] else "/"
            refresh()

        listbox.bind("<Double-Button-1>", on_double)
        tk.Button(w.body, text="Up", width=8, command=go_up).pack(side="left")
        refresh()