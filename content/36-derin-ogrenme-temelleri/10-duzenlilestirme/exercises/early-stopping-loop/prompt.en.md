The big network is trained on 80 examples and the validation loss is measured every
epoch. Write early stopping at the end of the loop: if the loss is below the best,
update `best`, `best_epoch` and reset `waited`; otherwise grow `waited` and leave
the loop when it reaches `patience`.

**Expected output:**

```
True True
True
```
