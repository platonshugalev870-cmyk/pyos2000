import time
from config.hardware_db import HARDWARE_DB


class HardwareScan:
    def __init__(self, logger, colors):
        self.logger = logger
        self.colors = colors
        self.db = HARDWARE_DB
        self.devices = []

    def scan_gui(self, on_line, on_finish):
        self.devices = []
        for category, items in self.db.items():
            on_line(f"Scanning {category}...")
            for item in items:
                if item.get("detected", True):
                    entry = {
                        "category": category,
                        "name": item["name"],
                        "vendor": item["vendor"],
                        "resource": item["resource"],
                        "driver": item["driver"],
                        "detected": True,
                    }
                    self.devices.append(entry)
                    on_line(f"  + {item['name']:<34} [{item['vendor']}]")
            on_line("")
        on_line(f"Detection complete. Found {len(self.devices)} device(s).")
        on_finish()