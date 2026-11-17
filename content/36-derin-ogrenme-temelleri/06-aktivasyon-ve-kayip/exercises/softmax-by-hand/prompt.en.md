`to_probabilities(logits)` should turn each row into probabilities: exponentiate with
`torch.exp`, divide by the row total. Return the result as a list of lists with 3
places. Do not use `torch.softmax`.

**Expected output:**

```
[[0.659, 0.242, 0.099]]
[[0.5, 0.5], [0.998, 0.002]]
```
