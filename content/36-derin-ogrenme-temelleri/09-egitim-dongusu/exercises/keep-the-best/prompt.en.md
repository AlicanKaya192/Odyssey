`restore_best` saves the best state while the weight is 1, sets the weight to 5,
then goes back to the best state. But it prints 5: the saved dictionary changed
together with the model. Fix the saving line.

**Expected output:**

```
1.0
```
