`early_stop(val_losses, patience)` should go through the epochs' validation
losses in order (epochs start at 1). If a loss is below the best, it becomes
the best and the counter resets; otherwise the counter goes up, and on
reaching `patience` training stops. Return `[best epoch, stop epoch]`; if it
never stops, the stop epoch is the last epoch.

**Expected output:**

```
[3, 6]
```
