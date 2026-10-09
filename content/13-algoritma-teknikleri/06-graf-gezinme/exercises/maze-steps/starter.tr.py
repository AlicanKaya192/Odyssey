from collections import deque


def maze_steps(maze):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    # Dort yonu dene.
    return -1


print(maze_steps(["..#", ".#.", "..."]))
print(maze_steps([".#", "#."]))
big = ["".join("#" if (r * 7 + c * 13) % 11 == 0 and (r, c) != (0, 0) else "." for c in range(300)) for r in range(300)]
print(maze_steps(big))
