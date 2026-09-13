import sys
from boot.post import POST
from boot.bios import BIOS
from boot.bootloader import Bootloader
from utils.logger import Logger
from utils.colors import Colors


def main():
    logger = Logger()
    colors = Colors()
    colors.clear()
    post = POST(logger)
    post.run()
    bios = BIOS(logger, colors)
    bios.show_splash()
    bootloader = Bootloader(logger, colors)
    bootloader.start()


if __name__ == "__main__":
    main()