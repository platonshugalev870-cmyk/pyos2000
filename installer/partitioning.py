class Partitioning:
    def __init__(self, logger, colors):
        self.logger = logger
        self.colors = colors

    def run(self):
        return [{"letter": "C:", "size": 2048, "fs": "PyFAT16", "active": True}]