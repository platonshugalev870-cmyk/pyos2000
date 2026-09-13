import os
import json


class VFS:
    def __init__(self, root="pyos_fs"):
        self.root = root
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        self.meta_path = os.path.join(self.root, ".meta.json")
        self.meta = self.load_meta()

    def load_meta(self):
        if os.path.exists(self.meta_path):
            with open(self.meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_meta(self):
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, indent=2, ensure_ascii=False)

    def full(self, path):
        clean = path.lstrip("/").replace("/", os.sep)
        return os.path.join(self.root, clean)

    def exists(self, path):
        return os.path.exists(self.full(path))

    def mkdir(self, path):
        p = self.full(path)
        if not os.path.exists(p):
            os.makedirs(p)
        self.meta[path] = {"type": "dir"}
        self.save_meta()

    def write(self, path, data):
        p = self.full(path)
        parent = os.path.dirname(p)
        if not os.path.exists(parent):
            os.makedirs(parent)
        with open(p, "w", encoding="utf-8") as f:
            f.write(str(data))
        self.meta[path] = {"type": "file", "size": len(str(data))}
        self.save_meta()

    def read(self, path):
        p = self.full(path)
        if not os.path.exists(p):
            return None
        with open(p, "r", encoding="utf-8") as f:
            return f.read()

    def ls(self, path):
        p = self.full(path)
        if not os.path.exists(p):
            return []
        return os.listdir(p)

    def delete(self, path):
        p = self.full(path)
        if os.path.isfile(p):
            os.remove(p)
        elif os.path.isdir(p):
            import shutil
            shutil.rmtree(p)
        if path in self.meta:
            del self.meta[path]
            self.save_meta()