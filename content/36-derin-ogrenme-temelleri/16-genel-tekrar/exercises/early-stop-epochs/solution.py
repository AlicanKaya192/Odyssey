def early_stop(val_losses, patience):
    best, best_epoch, waited = float("inf"), 0, 0
    for epoch, loss in enumerate(val_losses, start=1):
        if loss < best:
            best, best_epoch, waited = loss, epoch, 0
        else:
            waited += 1
            if waited == patience:
                return [best_epoch, epoch]
    return [best_epoch, len(val_losses)]

print(early_stop([0.9, 0.7, 0.6, 0.65, 0.62, 0.61, 0.7], 3))
