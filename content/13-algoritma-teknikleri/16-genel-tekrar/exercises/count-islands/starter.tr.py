from collections import deque


def count_islands(grid):
    seen = set()
    islands = 0
    # Her ziyaret edilmemis "1"den BFS.
    return islands

grid = ["11000",
        "11010",
        "00011",
        "10000"]
print(count_islands(grid))
print(count_islands(["000", "000"]))
big = ["10" * 150 if r % 2 == 0 else "0" * 300 for r in range(300)]
print(count_islands(big))
