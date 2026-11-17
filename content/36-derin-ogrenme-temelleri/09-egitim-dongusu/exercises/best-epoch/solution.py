def best_epoch(history):
    best, best_loss = 1, history[0][1]
    for epoch, (train_loss, val_loss) in enumerate(history, start=1):
        if val_loss < best_loss:
            best, best_loss = epoch, val_loss
    return best

history = [[0.9, 0.8], [0.6, 0.5], [0.4, 0.45], [0.3, 0.47], [0.2, 0.52]]
print(best_epoch(history))
