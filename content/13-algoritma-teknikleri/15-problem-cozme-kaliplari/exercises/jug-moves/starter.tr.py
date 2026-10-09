from collections import deque


def min_moves(a, b, goal):
    dist = {(0, 0): 0}
    queue = deque([(0, 0)])
    # Kuyruk bosalana kadar: hedef mi? Alti hamleyi dene.
    return -1

print(min_moves(3, 5, 4))
print(min_moves(2, 4, 3))
print(min_moves(7, 11, 6))
