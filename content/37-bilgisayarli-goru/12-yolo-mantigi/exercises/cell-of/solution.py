def cell_of(box, size, S):
    cell = size / S
    cx = (box[0] + box[2]) / 2
    cy = (box[1] + box[3]) / 2
    return [int(cy // cell), int(cx // cell)]

print(cell_of([20, 9, 23, 14], 32, 4))
print(cell_of([0, 0, 7, 7], 32, 4))
print(cell_of([30, 30, 32, 32], 32, 4))
