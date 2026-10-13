def lstm_memory(forgets, writes, news):
    c, cells = 0.0, []
    for f, i, g in zip(forgets, writes, news):
        c = f * c + i * g
        cells.append(round(c, 3))
    return cells

print(lstm_memory([1.0, 1.0, 1.0], [1.0, 0.0, 0.0], [0.8, 0.0, 0.0]))
print(lstm_memory([1.0, 0.5, 0.0], [1.0, 0.0, 1.0], [1.0, 0.0, -0.3]))
