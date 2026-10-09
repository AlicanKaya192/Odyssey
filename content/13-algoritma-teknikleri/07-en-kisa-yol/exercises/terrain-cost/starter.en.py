import heapq
import math


def min_cost(grid):
    rows, cols = len(grid), len(grid[0])
    best = {(0, 0): grid[0][0]}
    heap = [(grid[0][0], 0, 0)]
    # Dijkstra: four neighbours, weight = the cost of the cell entered.
    return best.get((rows - 1, cols - 1))


print(min_cost([[1, 3, 1], [1, 5, 1], [4, 2, 1]]))
print(min_cost([[1, 9, 1, 1], [1, 9, 1, 9], [1, 1, 1, 9], [9, 9, 1, 1]]))
big = [[(r * 37 + c * 91) % 9 + 1 for c in range(150)] for r in range(150)]
print(min_cost(big))
