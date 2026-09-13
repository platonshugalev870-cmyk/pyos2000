from drivers.keyboard import KeyboardDriver
from drivers.mouse import MouseDriver
from drivers.vga import VGADriver
from drivers.sound import SoundDriver
from drivers.network import NetworkDriver
from drivers.disk import DiskDriver


class DriverManager:
    def __init__(self, logger, colors, vfs):
        self.logger = logger
        self.colors = colors
        self.vfs = vfs
        self.drivers = {}

    def load_all(self):
        self.drivers["keyboard"] = KeyboardDriver()
        self.drivers["mouse"] = MouseDriver()
        self.drivers["vga"] = VGADriver()
        self.drivers["sound"] = SoundDriver()
        self.drivers["network"] = NetworkDriver()
        self.drivers["disk"] = DiskDriver()
        for driver in self.drivers.values():
            driver.load()

    def count(self):
        return len([d for d in self.drivers.values() if d.loaded])

    def get(self, name):
        return self.drivers.get(name)

    def list(self):
        return [d.info() for d in self.drivers.values()]