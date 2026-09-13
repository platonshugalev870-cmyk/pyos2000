import time
from utils.animate import typewriter
from kernel.scheduler import Scheduler
from kernel.memory import MemoryManager
from kernel.interrupts import InterruptTable
from kernel.syscalls import SyscallTable
from drivers.manager import DriverManager
from registry.registry import Registry
from gui.desktop import Desktop


class Kernel:
    def __init__(self, logger, colors, vfs):
        self.logger = logger
        self.colors = colors
        self.vfs = vfs
        self.registry = Registry()
        self.scheduler = Scheduler()
        self.memory = MemoryManager(256)
        self.interrupts = InterruptTable()
        self.syscalls = SyscallTable()
        self.drivers = DriverManager(logger, colors, vfs)

    def boot(self):
        self.print_banner()
        self.load_kernel()
        self.init_memory()
        self.init_interrupts()
        self.init_syscalls()
        self.load_drivers()
        self.start_services()
        desktop = Desktop(self.logger, self.colors, self.vfs, self.registry)
        desktop.run()

    def print_banner(self):
        typewriter(self.colors.c("  PyOS 2000", self.colors.bold + self.colors.cyan), delay=0.02)
        typewriter(self.colors.c("  Copyright (C) 2000 PySoft Corporation", self.colors.white), delay=0.012)
        print()

    def load_kernel(self):
        info = self.vfs.read("/system/version.txt") or "PyOS 2000"
        typewriter(self.colors.c(f"  Kernel: {info}", self.colors.green), delay=0.012)
        time.sleep(0.15)

    def init_memory(self):
        typewriter(self.colors.c(f"  Memory: {self.memory.total} MB detected", self.colors.white), delay=0.01)
        self.memory.alloc("kernel", 8)
        time.sleep(0.12)

    def init_interrupts(self):
        self.interrupts.register(0, "Divide Error")
        self.interrupts.register(1, "Debug")
        self.interrupts.register(8, "Timer")
        self.interrupts.register(9, "Keyboard")
        self.interrupts.register(13, "General Protection")
        self.interrupts.register(14, "Page Fault")
        self.interrupts.register(33, "Mouse")
        typewriter(self.colors.c("  Interrupts: IRQ table initialized", self.colors.white), delay=0.01)
        time.sleep(0.12)

    def init_syscalls(self):
        self.syscalls.register(1, "exit")
        self.syscalls.register(2, "fork")
        self.syscalls.register(3, "read")
        self.syscalls.register(4, "write")
        self.syscalls.register(5, "open")
        self.syscalls.register(6, "close")
        self.syscalls.register(39, "getpid")
        typewriter(self.colors.c("  Syscalls: 7 registered", self.colors.white), delay=0.01)
        time.sleep(0.12)

    def load_drivers(self):
        self.drivers.load_all()
        typewriter(self.colors.c(f"  Drivers: {self.drivers.count()} loaded", self.colors.white), delay=0.01)
        time.sleep(0.12)

    def start_services(self):
        services = ["EventLog", "PlugAndPlay", "TimeService", "PrintSpooler"]
        for s in services:
            typewriter(self.colors.c(f"  Service: {s} started", self.colors.white), delay=0.008)
            time.sleep(0.08)
        print()