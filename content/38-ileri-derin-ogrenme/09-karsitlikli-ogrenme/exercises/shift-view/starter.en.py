import torch


def shift_view(image, dx, dy, flip):
    # Write your code here
    return image

image = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
print(shift_view(image, 1, 0, False))
print(shift_view(image, 0, 1, True))
