`both_losses(logits, targets)` should return two losses: the right use (logits)
and the wrong use (first `torch.softmax`, then the same loss). Both with 3 places:
`[right, double softmax]`. Look at why the wrong use always stays large.

**Expected output:**

```
[0.036, 0.574]
[2.24, 1.38]
```
