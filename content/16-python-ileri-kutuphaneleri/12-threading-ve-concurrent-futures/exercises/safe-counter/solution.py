import threading
import time


class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def add_many(self, n):
        for _ in range(n):
            with self.lock:
                current = self.value
                time.sleep(0)
                self.value = current + 1


counter = Counter()
workers = [threading.Thread(target=counter.add_many, args=(500,)) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print(counter.value)
