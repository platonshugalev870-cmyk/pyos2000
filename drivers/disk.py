from drivers.base import Driver


class DiskDriver(Driver):
    def __init__(self):
        super().__init__("PyIDE Controller", "1.2", "PySoft")
        self.disks = [{"name": "PYHDD-2000", "size": 2048}]

    def load(self):
        self.resources = {"irq": 14, "port": "0x1F0"}
        return super().load()