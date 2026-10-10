import queue
import threading

STOP = None


def square_all(numbers, n_workers):
    tasks = queue.Queue()
    results = queue.Queue()

    def worker():
        while True:
            item = tasks.get()
            if item is STOP:
                break
            results.put(item * item)

    workers = [threading.Thread(target=worker) for _ in range(n_workers)]
    for w in workers:
        w.start()
    for n in numbers:
        tasks.put(n)
    for _ in workers:
        tasks.put(STOP)
    for w in workers:
        w.join()
    return sorted(results.get() for _ in range(results.qsize()))

print(square_all([3, 1, 2], 2))
print(square_all(list(range(10)), 3))
