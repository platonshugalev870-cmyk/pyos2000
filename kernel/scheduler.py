import time


class Process:
    def __init__(self, pid, name, priority=5):
        self.pid = pid
        self.name = name
        self.priority = priority
        self.state = "READY"
        self.cpu_time = 0
        self.created = time.time()


class Scheduler:
    def __init__(self):
        self.processes = []
        self.current = None
        self.next_pid = 1

    def spawn(self, name, priority=5):
        p = Process(self.next_pid, name, priority)
        self.next_pid += 1
        self.processes.append(p)
        return p

    def kill(self, pid):
        self.processes = [p for p in self.processes if p.pid != pid]

    def schedule(self):
        ready = [p for p in self.processes if p.state == "READY"]
        if not ready:
            return None
        ready.sort(key=lambda p: -p.priority)
        self.current = ready[0]
        self.current.state = "RUNNING"
        return self.current

    def ps(self):
        return [(p.pid, p.name, p.state, round(p.cpu_time, 3)) for p in self.processes]