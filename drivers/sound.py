from drivers.base import Driver


class SoundDriver(Driver):
    def __init__(self):
        super().__init__("PySoundBlaster 16", "2.1", "PySoft")
        self.volume = 80

    def load(self):
        self.resources = {"irq": 5, "dma": 1, "port": "0x220"}
        return super().load()