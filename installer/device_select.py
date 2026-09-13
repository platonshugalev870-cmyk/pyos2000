class DeviceSelect:
    def __init__(self, logger, colors, devices):
        self.logger = logger
        self.colors = colors
        self.devices = devices

    def run(self):
        return self.devices