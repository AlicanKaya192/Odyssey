import torch


def channels_first(img):
    return []

img = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
result = channels_first(img)
print(len(result), len(result[0]), len(result[0][0]))
print(result[0])
