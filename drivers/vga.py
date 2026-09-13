from drivers.base import Driver


class VGADriver(Driver):
    def __init__(self):
        super().__init__("PyVGA 4MB", "3.0", "PySoft")
        self.modes = ["640x480x16", "800x600x256", "1024x768x256"]
        self.current = 0

    def load(self):
        self.resources = {"irq": 10, "mem": "0xA0000", "vram": "4MB"}
        return super().load()