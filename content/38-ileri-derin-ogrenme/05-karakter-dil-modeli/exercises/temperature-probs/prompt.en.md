`temperature_probs(logits, temp)` should divide the logits by `temp`, take the
softmax and return the probabilities as a list with 3 places.

**Expected output:**

```
[0.864, 0.117, 0.019]
[0.502, 0.304, 0.194]
```
