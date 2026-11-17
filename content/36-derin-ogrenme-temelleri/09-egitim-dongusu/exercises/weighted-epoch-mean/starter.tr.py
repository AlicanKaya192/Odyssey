def epoch_mean(batch_losses, batch_sizes):
    return [0.0, 0.0]

print(epoch_mean([0.5, 0.25, 1.0], [32, 32, 4]))
