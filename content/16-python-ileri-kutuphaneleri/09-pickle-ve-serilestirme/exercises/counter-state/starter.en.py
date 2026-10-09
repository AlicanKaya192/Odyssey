import pickle
import threading


class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def add(self):
        with self.lock:
            self.count += 1


c = Counter()
c.add()
c.add()
back = pickle.loads(pickle.dumps(c))
back.add()
print(back.count, type(back.lock).__name__)
