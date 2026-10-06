height = 7
middle = height // 2

for row in range(height):
    if row <= middle:
        distance = middle - row
    else:
        distance = row - middle
    spaces = distance
    stars = height - 2 * distance
    print(" " * spaces + "*" * stars)
