from collections import deque


def maze_steps(maze):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        r, c, steps = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return steps
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == "." and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc, steps + 1))
    return -1


print(maze_steps(["..#", ".#.", "..."]))
print(maze_steps([".#", "#."]))
big = ["".join("#" if (r * 7 + c * 13) % 11 == 0 and (r, c) != (0, 0) else "." for c in range(300)) for r in range(300)]
print(maze_steps(big))
