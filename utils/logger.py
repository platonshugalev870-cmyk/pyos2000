from datetime import datetime


class Logger:
    def __init__(self):
        self.entries = []

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.entries.append(entry)
        return entry

    def info(self, message):
        return self.log(message, "INFO")

    def warn(self, message):
        return self.log(message, "WARN")

    def error(self, message):
        return self.log(message, "ERROR")

    def dump(self):
        return "\n".join(self.entries)