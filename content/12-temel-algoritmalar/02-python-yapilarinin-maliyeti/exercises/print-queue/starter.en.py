from collections import deque


def print_order(jobs):
    queue = deque()
    for name, pages in jobs:
        queue.append([name, pages])
    finished = []
    # Until the queue is empty: take from the front, print at most 2 pages,
    # put it back at the end if it is not finished.

    return finished


print(print_order([["a", 3], ["b", 1], ["c", 2]]))
print(print_order([["report", 5], ["memo", 1]]))
