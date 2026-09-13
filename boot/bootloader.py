import sys
import time
from utils.animate import typewriter
from installer.wizard import InstallWizard
from kernel.kernel import Kernel
from fs.vfs import VFS


class Bootloader:
    def __init__(self, logger, colors):
        self.logger = logger
        self.colors = colors
        self.vfs = VFS()
        self.installed = self.vfs.exists("/system/pyos.sys")

    def start(self):
        self.colors.clear()
        print()
        typewriter("  Booting from Hard Disk...", delay=0.02)
        time.sleep(0.5)
        print()
        if not self.installed:
            typewriter("  Operating System not found.", delay=0.02)
            typewriter("  Insert setup media and reboot.", delay=0.02)
            print()
            time.sleep(0.6)
            self.show_install_prompt()
        else:
            self.load_installed()

    def show_install_prompt(self):
        print(self.colors.c("  [1] Install PyOS 2000", self.colors.cyan))
        print(self.colors.c("  [2] Exit Setup", self.colors.cyan))
        print()
        choice = input(self.colors.c("  Choice: ", self.colors.yellow))
        if choice.strip() == "1":
            wizard = InstallWizard(self.logger, self.colors, self.vfs)
            wizard.run()
        else:
            print(self.colors.c("  Halting system.", self.colors.red))
            sys.exit(0)

    def load_installed(self):
        typewriter("  Loading PyOS 2000...", delay=0.015)
        time.sleep(0.3)
        typewriter("  Reading /system/pyos.sys", delay=0.012)
        time.sleep(0.2)
        typewriter("  Loading kernel modules...", delay=0.012)
        time.sleep(0.2)
        typewriter("  Starting services...", delay=0.012)
        time.sleep(0.3)
        print()
        kernel = Kernel(self.logger, self.colors, self.vfs)
        kernel.boot()