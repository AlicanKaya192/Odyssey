def lstm_memory(forgets, writes, news):
    return []

print(lstm_memory([1.0, 1.0, 1.0], [1.0, 0.0, 0.0], [0.8, 0.0, 0.0]))
print(lstm_memory([1.0, 0.5, 0.0], [1.0, 0.0, 1.0], [1.0, 0.0, -0.3]))
