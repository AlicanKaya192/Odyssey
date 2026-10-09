from collections import deque


def print_order(jobs):
    queue = deque()
    for name, pages in jobs:
        queue.append([name, pages])
    finished = []
    while queue:
        name, pages = queue.popleft()
        pages -= 2
        if pages > 0:
            queue.append([name, pages])
        else:
            finished.append(name)
    return finished


print(print_order([["a", 3], ["b", 1], ["c", 2]]))
print(print_order([["report", 5], ["memo", 1]]))
