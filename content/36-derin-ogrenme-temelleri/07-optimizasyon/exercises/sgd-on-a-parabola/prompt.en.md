`descend(start, lr, steps)` should shrink the loss `(w − 3)²` with
`torch.optim.SGD` for `steps` steps and return the final `w` with 4 places. Four
steps in the loop: `zero_grad`, the loss, `backward`, `step`.

**Expected output:**

```
2.6779
3.0
```
