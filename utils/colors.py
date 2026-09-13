import os


class Colors:
    def __init__(self):
        self.reset = "\033[0m"
        self.bold = "\033[1m"
        self.red = "\033[31m"
        self.green = "\033[32m"
        self.yellow = "\033[33m"
        self.blue = "\033[34m"
        self.magenta = "\033[35m"
        self.cyan = "\033[36m"
        self.white = "\033[37m"

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def c(self, text, color):
        return f"{color}{text}{self.reset}"