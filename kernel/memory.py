class MemoryManager:
    def __init__(self, total_mb):
        self.total = total_mb
        self.blocks = []
        self.used = 0

    def alloc(self, name, size):
        if self.used + size > self.total:
            return None
        block = {"name": name, "size": size, "addr": self.used}
        self.blocks.append(block)
        self.used += size
        return block

    def free(self, name):
        before = len(self.blocks)
        self.blocks = [b for b in self.blocks if b["name"] != name]
        freed = before - len(self.blocks)
        if freed:
            self.used = sum(b["size"] for b in self.blocks)
        return freed

    def stats(self):
        return {
            "total": self.total,
            "used": self.used,
            "free": self.total - self.used,
            "blocks": len(self.blocks),
        }