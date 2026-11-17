def decode_grid(output, S, size, threshold):
    cell = size / S
    found = []
    for row in range(S):
        for col in range(S):
            values = output[row][col]
            probs = values[5:]
            label = probs.index(max(probs))
            score = values[0] * probs[label]
            if score < threshold:
                continue
            cx = (col + values[1]) * cell
            cy = (row + values[2]) * cell
            w, h = values[3] * size, values[4] * size
            corners = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
            found.append(corners + [label, round(score, 2)])
    return found

empty = [0.0] * 7
grid = [[empty, [0.9, 0.5, 0.5, 0.5, 0.5, 0.1, 0.9]],
        [[0.6, 0.25, 0.75, 0.25, 0.25, 0.7, 0.3], [0.4, 0.5, 0.5, 0.5, 0.5, 1.0, 0.0]]]
for box in decode_grid(grid, 2, 16, 0.4):
    print(box)
