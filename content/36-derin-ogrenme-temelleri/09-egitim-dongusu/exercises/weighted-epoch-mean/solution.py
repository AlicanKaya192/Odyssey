def epoch_mean(batch_losses, batch_sizes):
    weighted = sum(l * n for l, n in zip(batch_losses, batch_sizes)) / sum(batch_sizes)
    naive = sum(batch_losses) / len(batch_losses)
    return [round(weighted, 4), round(naive, 4)]

print(epoch_mean([0.5, 0.25, 1.0], [32, 32, 4]))
