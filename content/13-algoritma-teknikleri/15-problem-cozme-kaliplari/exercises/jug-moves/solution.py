from collections import deque


def min_moves(a, b, goal):
    dist = {(0, 0): 0}
    queue = deque([(0, 0)])
    while queue:
        x, y = queue.popleft()
        if goal in (x, y):
            return dist[(x, y)]
        pour_xy = min(x, b - y)
        pour_yx = min(y, a - x)
        for nxt in [(a, y), (x, b), (0, y), (x, 0),
                    (x - pour_xy, y + pour_xy), (x + pour_yx, y - pour_yx)]:
            if nxt not in dist:
                dist[nxt] = dist[(x, y)] + 1
                queue.append(nxt)
    return -1

print(min_moves(3, 5, 4))
print(min_moves(2, 4, 3))
print(min_moves(7, 11, 6))
