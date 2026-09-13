from config.versions import VERSIONS


class VersionSelect:
    def __init__(self, logger, colors):
        self.logger = logger
        self.colors = colors
        self.versions = VERSIONS