def decode_cell(row, col, values, S, size):
    cell = size / S
    probs = values[5:]
    label = probs.index(max(probs))
    cx = (col + values[1]) * cell
    cy = (row + values[2]) * cell
    w = values[3] * size
    h = values[4] * size
    score = round(values[0] * probs[label], 2)
    return [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, label, score]

print(decode_cell(1, 2, [1.0, 0.5, 0.5, 0.25, 0.5, 0.1, 0.8, 0.1], 4, 32))
print(decode_cell(0, 0, [0.5, 0.25, 0.75, 0.125, 0.125, 0.0, 0.0, 1.0], 4, 32))
