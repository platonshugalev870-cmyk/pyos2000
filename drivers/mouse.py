from drivers.base import Driver


class MouseDriver(Driver):
    def __init__(self):
        super().__init__("PyPS/2 Mouse", "1.5", "PySoft")
        self.x = 0
        self.y = 0

    def load(self):
        self.resources = {"irq": 12, "port": "0x60"}
        return super().load()