import torch


def encode(boxes, S, size, C):
    cell = size / S
    target = torch.zeros(S, S, 5 + C)
    for x1, y1, x2, y2, label in boxes:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        row, col = int(cy // cell), int(cx // cell)
        target[row, col, 0] = 1
        target[row, col, 1] = cx / cell - col
        target[row, col, 2] = cy / cell - row
        target[row, col, 3] = (x2 - x1) / size
        target[row, col, 4] = (y2 - y1) / size
        target[row, col, 5 + label] = 1
    return target.tolist()

target = encode([[2, 4, 10, 12, 0], [8, 0, 16, 4, 1]], 2, 16, 2)
for row in target:
    for cell in row:
        print(cell)
