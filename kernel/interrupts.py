class InterruptTable:
    def __init__(self):
        self.handlers = {}

    def register(self, irq, name, handler=None):
        self.handlers[irq] = {"name": name, "handler": handler}

    def unregister(self, irq):
        if irq in self.handlers:
            del self.handlers[irq]

    def raise_irq(self, irq):
        h = self.handlers.get(irq)
        if h and h["handler"]:
            return h["handler"]()
        return None

    def list(self):
        return sorted(self.handlers.items())