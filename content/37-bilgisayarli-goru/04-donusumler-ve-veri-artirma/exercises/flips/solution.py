def flips(img):
    horizontal = [row[::-1] for row in img]
    vertical = img[::-1]
    return horizontal, vertical

h, v = flips([[1, 2, 3], [4, 5, 6]])
print(h)
print(v)
