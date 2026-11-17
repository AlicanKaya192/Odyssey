class EarlyStopping:
    def __init__(self, patience):
        self.patience = patience
        self.best, self.waited = float("inf"), 0

    def step(self, val_loss):
        return False

def stop_epoch(losses, patience):
    stopper = EarlyStopping(patience)
    for epoch, loss in enumerate(losses, start=1):
        if stopper.step(loss):
            return epoch
    return None

print(stop_epoch([0.9, 0.7, 0.6, 0.62, 0.61, 0.65, 0.5], 3))
print(stop_epoch([0.5, 0.4, 0.3], 2))
