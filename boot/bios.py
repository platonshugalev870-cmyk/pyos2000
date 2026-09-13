import time
from utils.animate import typewriter_lines, progress_dots


class BIOS:
    def __init__(self, logger, colors):
        self.logger = logger
        self.colors = colors
        self.splash_lines = [
            "  _____       _____  _____  ",
            " |  __ \\     / ____|/ ____| ",
            " | |__) |_ _| |    | (___   ",
            " |  ___/ _` | |     \\___ \\  ",
            " | |  | (_| | |____ ____) | ",
            " |_|   \\__,_|\\_____|_____/  ",
            "                            ",
            "     PyOS 2000 Edition      ",
        ]

    def show_splash(self):
        self.colors.clear()
        print()
        for line in self.splash_lines:
            print(self.colors.c(line, self.colors.cyan))
            time.sleep(0.08)
        print()
        print(self.colors.c("  PySoft Corporation (C) 2000", self.colors.white))
        print()
        progress_dots("  Initializing", count=3, delay=0.3)
        time.sleep(0.4)