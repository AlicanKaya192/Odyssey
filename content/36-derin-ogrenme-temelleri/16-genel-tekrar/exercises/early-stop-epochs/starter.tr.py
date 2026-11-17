def early_stop(val_losses, patience):
    return [0, 0]

print(early_stop([0.9, 0.7, 0.6, 0.65, 0.62, 0.61, 0.7], 3))
