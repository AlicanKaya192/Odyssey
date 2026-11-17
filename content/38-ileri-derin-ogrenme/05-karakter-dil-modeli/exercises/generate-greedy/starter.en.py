import torch


def generate_greedy(table, start, n):
    # Write your code here
    return []

table = [[0.0, 3.0, 1.0],
         [0.5, 0.0, 2.0],
         [4.0, 1.0, 0.0]]
print(generate_greedy(table, 0, 5))
print(generate_greedy(table, 2, 3))
