import time
from utils.animate import typewriter, typewriter_lines


class POST:
    def __init__(self, logger):
        self.logger = logger
        self.checks = [
            ("CPU", "PyCPU 2000 @ 500 MHz"),
            ("RAM", "262144 KB OK"),
            ("Cache", "512 KB"),
            ("Video", "PyVGA 4MB"),
            ("Keyboard", "OK"),
            ("Mouse", "OK"),
            ("Floppy", "1.44MB"),
            ("HDD Primary Master", "PYHDD-2000 2048MB"),
            ("HDD Primary Slave", "None"),
            ("CD-ROM", "PYCD-52X"),
            ("Sound", "PySoundBlaster 16"),
            ("Network", "PyEthernet 10/100"),
        ]

    def run(self):
        typewriter("\033[37mPyBIOS (C) 2000 PySoft Inc.\033[0m", delay=0.015)
        typewriter("\033[37mVersion 2.00.04\033[0m", delay=0.015)
        print()
        time.sleep(0.3)
        for name, value in self.checks:
            line = f"{name:<24} : {value}"
            typewriter("\033[37m" + line + "\033[0m", delay=0.006)
            time.sleep(0.06)
        print()
        time.sleep(0.3)