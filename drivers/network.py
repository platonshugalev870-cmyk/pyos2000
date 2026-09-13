from drivers.base import Driver


class NetworkDriver(Driver):
    def __init__(self):
        super().__init__("PyEthernet 10/100", "1.0", "PySoft")
        self.ip = "192.168.0.1"
        self.mac = "00:50:56:AA:BB:CC"

    def load(self):
        self.resources = {"irq": 9, "port": "0x300"}
        return super().load()