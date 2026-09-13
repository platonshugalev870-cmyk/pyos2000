from tqdm import tqdm


class Progress:
    def __init__(self, logger, colors):
        self.logger = logger
        self.colors = colors
        self.steps = [
            "Initializing filesystem",
            "Installing kernel",
            "Installing drivers",
            "Registering components",
            "Building registry hive",
            "Setting up user profile",
            "Optimizing system files",
            "Finalizing installation",
        ]

    def run_gui(self, step_callback, on_finish):
        bar = tqdm(self.steps, desc="Installing PyOS 2000", ncols=70, ascii=True)
        for idx, name in enumerate(bar):
            bar.set_description(name)
            step_callback(idx, name, len(self.steps))
        bar.close()
        on_finish()