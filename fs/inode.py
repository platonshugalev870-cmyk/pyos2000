import time


class Inode:
    def __init__(self, name, size, is_dir=False):
        self.name = name
        self.size = size
        self.is_dir = is_dir
        self.created = time.time()
        self.modified = time.time()

    def touch(self):
        self.modified = time.time()