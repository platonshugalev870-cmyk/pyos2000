from drivers.base import Driver


class KeyboardDriver(Driver):
    def __init__(self):
        super().__init__("PyPS/2 Keyboard", "2.0", "PySoft")
        self.layout = "US"

    def load(self):
        self.resources = {"irq": 1, "port": "0x60"}
        return super().load()