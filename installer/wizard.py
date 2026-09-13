import tkinter as tk
from tkinter import messagebox
from installer.hardware_scan import HardwareScan
from installer.device_select import DeviceSelect
from installer.version_select import VersionSelect
from installer.partitioning import Partitioning
from installer.filecopy import FileCopy
from installer.progress import Progress
from registry.registry import Registry
from utils.animate import gui_type_lines, fade_in_window, pulse_widget


class InstallWizard:
    def __init__(self, logger, colors, vfs):
        self.logger = logger
        self.colors = colors
        self.vfs = vfs
        self.registry = Registry()
        self.state = {}
        self.root = None

    def run(self):
        self.root = tk.Tk()
        self.root.title("PyOS 2000 Setup")
        self.root.geometry("720x520")
        self.root.configure(bg="#008080")
        self.root.resizable(False, False)
        self.welcome_screen()
        fade_in_window(self.root)
        self.root.mainloop()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def header(self, title, step, total):
        top = tk.Frame(self.root, bg="#000080", height=70)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(
            top, text="PyOS 2000 Setup Wizard",
            bg="#000080", fg="white",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 0))
        tk.Label(
            top, text=f"Step {step} of {total}: {title}",
            bg="#000080", fg="#c0c0c0",
            font=("Arial", 11)
        ).pack(anchor="w", padx=20)

    def footer(self, on_next, next_text="Next >"):
        bar = tk.Frame(self.root, bg="#c0c0c0", height=50)
        bar.pack(side="bottom", fill="x")
        bar.pack_propagate(False)
        tk.Button(
            bar, text=next_text, width=12,
            font=("Arial", 10), command=on_next
        ).pack(side="right", padx=10, pady=10)
        tk.Button(
            bar, text="< Back", width=12,
            font=("Arial", 10), state="disabled"
        ).pack(side="right", padx=5, pady=10)
        tk.Button(
            bar, text="Cancel", width=12,
            font=("Arial", 10), command=self.root.destroy
        ).pack(side="left", padx=10, pady=10)

    def welcome_screen(self):
        self.clear()
        self.header("Welcome", 1, 7)
        body = tk.Frame(self.root, bg="#008080")
        body.pack(fill="both", expand=True, padx=30, pady=20)
        tk.Label(
            body, text="Welcome to PyOS 2000 Setup",
            bg="#008080", fg="white",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(0, 15))
        text_widget = tk.Text(
            body, bg="#008080", fg="white", bd=0,
            font=("Arial", 11), wrap="word", height=8, width=70,
            highlightthickness=0
        )
        text_widget.pack(anchor="w", fill="x")
        lines = [
            "This wizard will guide you through the installation of",
            "the PyOS 2000 operating system on your computer.",
            "",
            "Please read the license agreement carefully before continuing.",
            "",
            "By clicking Next, you agree to the terms of the PySoft",
            "End User License Agreement.",
        ]
        gui_type_lines(text_widget, lines, delay=0, line_delay=180)
        self.footer(self.run_hardware_scan)

    def run_hardware_scan(self):
        self.clear()
        self.header("Hardware Detection", 2, 7)
        body = tk.Frame(self.root, bg="#008080")
        body.pack(fill="both", expand=True, padx=30, pady=20)
        tk.Label(
            body, text="Scanning hardware...",
            bg="#008080", fg="white",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")
        log = tk.Text(body, height=16, width=80, bg="#000000", fg="#00ff00", font=("Consolas", 9))
        log.pack(pady=10)
        scanner = HardwareScan(self.logger, self.colors)

        def on_line(line):
            log.insert("end", line + "\n")
            log.see("end")
            self.root.update()

        def finish():
            self.state["devices"] = scanner.devices
            self.run_device_select()

        scanner.scan_gui(on_line, finish)

    def run_device_select(self):
        self.clear()
        self.header("Select Devices", 3, 7)
        body = tk.Frame(self.root, bg="#008080")
        body.pack(fill="both", expand=True, padx=30, pady=15)
        tk.Label(
            body, text="Select drivers to install:",
            bg="#008080", fg="white",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 10))
        vars_map = {}
        canvas_frame = tk.Frame(body, bg="#008080")
        canvas_frame.pack(fill="both", expand=True)
        for d in self.state["devices"]:
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(
                canvas_frame,
                text=f"{d['name']:<34} {d['driver']:<14} {d['resource']}",
                variable=var, bg="#008080", fg="white",
                selectcolor="#004040",
                activebackground="#008080", activeforeground="white",
                font=("Consolas", 10), anchor="w"
            )
            chk.pack(fill="x")
            vars_map[d["name"]] = var

        def on_next():
            self.state["selected_devices"] = [
                d for d in self.state["devices"] if vars_map[d["name"]].get()
            ]
            self.run_version_select()

        self.footer(on_next)

    def run_version_select(self):
        self.clear()
        self.header("Select Version", 4, 7)
        body = tk.Frame(self.root, bg="#008080")
        body.pack(fill="both", expand=True, padx=30, pady=15)
        tk.Label(
            body, text="Choose the edition of PyOS 2000:",
            bg="#008080", fg="white",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 10))
        selector = VersionSelect(self.logger, self.colors)
        var = tk.StringVar(value=selector.versions[0]["name"])
        desc_label = tk.Label(
            body, text=selector.versions[0]["long"],
            bg="#008080", fg="#ffff80",
            font=("Arial", 10, "italic"), wraplength=620, justify="left"
        )
        for v in selector.versions:
            rb = tk.Radiobutton(
                body, text=f"{v['name']:<28} {v['size']:>6} MB   {v['desc']}",
                variable=var, value=v["name"],
                bg="#008080", fg="white", selectcolor="#004040",
                activebackground="#008080", activeforeground="white",
                font=("Consolas", 10), anchor="w",
                command=lambda n=v["name"]: self.animate_desc(desc_label, n, selector)
            )
            rb.pack(fill="x")
        desc_label.pack(anchor="w", pady=15)

        def on_next():
            self.state["version"] = next(
                v for v in selector.versions if v["name"] == var.get()
            )
            self.run_partitioning()

        self.footer(on_next)

    def animate_desc(self, label, name, selector):
        text = next(x["long"] for x in selector.versions if x["name"] == name)
        label.config(text="")
        state = {"i": 0}

        def step():
            if state["i"] >= len(text):
                return
            label.config(text=label.cget("text") + text[state["i"]])
            state["i"] += 1
            label.after(12, step)

        step()

    def run_partitioning(self):
        self.clear()
        self.header("Disk Partitioning", 5, 7)
        body = tk.Frame(self.root, bg="#008080")
        body.pack(fill="both", expand=True, padx=30, pady=15)
        tk.Label(
            body, text="Disk 0: PYHDD-2000  2048 MB",
            bg="#008080", fg="white",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        part = Partitioning(self.logger, self.colors)
        choice = tk.IntVar(value=1)
        opts = [
            (1, "Use entire disk (recommended)"),
            (2, "Manual partitioning"),
            (3, "Keep existing filesystem"),
        ]
        for val, label in opts:
            tk.Radiobutton(
                body, text=label, variable=choice, value=val,
                bg="#008080", fg="white", selectcolor="#004040",
                activebackground="#008080", activeforeground="white",
                font=("Arial", 11), anchor="w"
            ).pack(fill="x", pady=3)
        info = tk.Text(body, height=8, width=80, bg="#000000", fg="#00ff00", font=("Consolas", 10))
        info.pack(pady=15)

        def refresh(*_):
            info.delete("1.0", "end")
            if choice.get() == 1 or choice.get() == 3:
                parts = [{"letter": "C:", "size": 2048, "fs": "PyFAT16", "active": True}]
            else:
                parts = [
                    {"letter": "C:", "size": 1024, "fs": "PyFAT16", "active": True},
                    {"letter": "D:", "size": 1024, "fs": "PyFAT16", "active": False},
                ]
            lines = ["Partition table:", ""]
            for p in parts:
                lines.append(f"  {p['letter']}  {p['fs']:<10} {p['size']:>6} MB  {'ACTIVE' if p['active'] else '':<6}")
            gui_type_lines(info, lines, line_delay=90)
            self.state["partitions"] = parts

        choice.trace_add("write", refresh)
        refresh()

        def on_next():
            self.run_filecopy()

        self.footer(on_next)

    def run_filecopy(self):
        self.clear()
        self.header("Copying Files", 6, 7)
        body = tk.Frame(self.root, bg="#008080")
        body.pack(fill="both", expand=True, padx=30, pady=15)
        tk.Label(
            body, text="Extracting files...",
            bg="#008080", fg="white",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        log = tk.Text(body, height=14, width=80, bg="#000000", fg="#00ff00", font=("Consolas", 9))
        log.pack(pady=10)
        copier = FileCopy(self.logger, self.colors, self.vfs)

        def on_line(line):
            log.insert("end", line + "\n")
            log.see("end")
            self.root.update()

        def finish():
            self.run_progress()

        copier.copy_gui(self.state, on_line, finish)

    def run_progress(self):
        self.clear()
        self.header("Installing", 7, 7)
        body = tk.Frame(self.root, bg="#008080")
        body.pack(fill="both", expand=True, padx=30, pady=20)
        tk.Label(
            body, text="Installing PyOS 2000...",
            bg="#008080", fg="white",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 20))
        status = tk.Label(body, text="Preparing...", bg="#008080", fg="white", font=("Arial", 10))
        status.pack(anchor="w")
        bar = tk.Canvas(body, width=600, height=30, bg="#000000", highlightthickness=0)
        bar.pack(pady=10)
        rect = bar.create_rectangle(2, 2, 2, 28, fill="#00c000", outline="")
        pct = tk.Label(body, text="0%", bg="#008080", fg="white", font=("Arial", 10, "bold"))
        pct.pack(anchor="w")

        progress = Progress(self.logger, self.colors)

        def step_callback(idx, name, total):
            ratio = (idx + 1) / total
            bar.coords(rect, 2, 2, 2 + int(596 * ratio), 28)
            pct.config(text=f"{int(ratio * 100)}%")
            status.config(text=name)
            self.root.update()

        def finish():
            messagebox.showinfo(
                "PyOS 2000",
                "Installation completed successfully!\n\n"
                "PyOS 2000 will now start."
            )
            self.registry.save("install_info", self.state)
            self.root.destroy()

        progress.run_gui(step_callback, finish)