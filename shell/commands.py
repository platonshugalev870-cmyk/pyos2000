class Commands:
    def __init__(self, shell):
        self.shell = shell

    def list(self):
        return [m for m in dir(self) if not m.startswith("_") and m != "list"]

    def dir(self, args):
        path = args[0] if args else self.shell.cwd
        items = self.shell.vfs.ls(path)
        for i in sorted(items):
            full = path.rstrip("/") + "/" + i
            meta = self.shell.vfs.meta.get(full, {})
            tag = "<DIR>" if meta.get("type") == "dir" else str(meta.get("size", 0))
            print(f"  {i:<30} {tag}")

    def type(self, args):
        if not args:
            return
        data = self.shell.vfs.read(args[0])
        if data is None:
            print(self.shell.colors.c("File Not Found", self.shell.colors.red))
            return
        print(data)

    def ver(self, args):
        print(self.shell.colors.c("PyOS 2000 [Version 2000.1.15]", self.shell.colors.cyan))

    def mem(self, args):
        for line in self.shell.logger.dump().splitlines():
            print(line)

    def physics(self, args):
        import tkinter as tk
        from apps.physics.physics import PhysicsApp
        root = tk.Tk()
        root.withdraw()
        PhysicsApp(root).run()
        root.mainloop()

    def history(self, args):
        import tkinter as tk
        from apps.history.history import HistoryApp
        root = tk.Tk()
        root.withdraw()
        HistoryApp(root).run()
        root.mainloop()