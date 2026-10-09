from collections import deque


def print_order(jobs):
    queue = deque()
    for name, pages in jobs:
        queue.append([name, pages])
    finished = []
    # Kuyruk bosalana kadar: bastan al, en fazla 2 sayfa bas,
    # bitmediyse sona geri ekle.

    return finished


print(print_order([["a", 3], ["b", 1], ["c", 2]]))
print(print_order([["report", 5], ["memo", 1]]))
