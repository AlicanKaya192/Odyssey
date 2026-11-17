def best_epoch(history):
    return len(history)

history = [[0.9, 0.8], [0.6, 0.5], [0.4, 0.45], [0.3, 0.47], [0.2, 0.52]]
print(best_epoch(history))
