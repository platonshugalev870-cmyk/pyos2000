class Driver:
    def __init__(self, name, version="1.0", vendor="PySoft"):
        self.name = name
        self.version = version
        self.vendor = vendor
        self.loaded = False
        self.resources = {}

    def load(self):
        self.loaded = True
        return True

    def unload(self):
        self.loaded = False
        return True

    def info(self):
        return {
            "name": self.name,
            "version": self.version,
            "vendor": self.vendor,
            "loaded": self.loaded,
        }