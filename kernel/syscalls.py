class SyscallTable:
    def __init__(self):
        self.calls = {}

    def register(self, num, name, func=None):
        self.calls[num] = {"name": name, "func": func}

    def invoke(self, num, *args):
        c = self.calls.get(num)
        if c and c["func"]:
            return c["func"](*args)
        return None

    def list(self):
        return sorted(self.calls.items())