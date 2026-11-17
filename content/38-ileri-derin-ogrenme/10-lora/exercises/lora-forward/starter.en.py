import torch


def lora_forward(x, W, b, A, B, alpha):
    # Write your code here
    return []

x = [[1.0, 2.0]]
W = [[1.0, 0.0], [0.0, 1.0]]
b = [0.0, 0.0]
A = [[1.0, 1.0]]
B = [[0.5], [0.0]]
print(lora_forward(x, W, b, A, B, 2.0))
