class FAT16:
    def __init__(self, size_mb):
        self.size_mb = size_mb
        self.cluster_size = 32
        self.total_clusters = (size_mb * 1024) // self.cluster_size
        self.fat = [0] * self.total_clusters
        self.label = "PYOS"

    def format(self, label="PYOS"):
        self.label = label
        self.fat[0] = 0xFFF8
        self.fat[1] = 0xFFFF
        return True