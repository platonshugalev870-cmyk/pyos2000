from shell.commands import Commands
from shell.builtins import BUILTINS


class Shell:
    def __init__(self, logger, colors, vfs, registry):
        self.logger = logger
        self.colors = colors
        self.vfs = vfs
        self.registry = registry
        self.cwd = "/"
        self.commands = Commands(self)
        self.running = True

    def run(self):
        print()
        print(self.colors.c("PyOS 2000 Command Interpreter", self.colors.bold + self.colors.cyan))
        while self.running:
            try:
                line = input(self.colors.c(f"{self.cwd}> ", self.colors.cyan))
            except (EOFError, KeyboardInterrupt):
                break
            self.execute(line)

    def execute(self, line):
        line = line.strip()
        if not line:
            return
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd in BUILTINS:
            BUILTINS[cmd](self, args)
        elif hasattr(self.commands, cmd):
            getattr(self.commands, cmd)(args)
        else:
            print(self.colors.c(f'Bad command: "{cmd}"', self.colors.red))

    def quit(self):
        self.running = False