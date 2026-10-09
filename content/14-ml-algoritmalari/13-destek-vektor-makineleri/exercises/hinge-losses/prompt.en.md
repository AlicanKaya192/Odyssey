Write the function `hinge_losses(y, scores)`: for each sample
`max(0, 1 − y · score)`; return `.round(3).tolist()`. Labels are `−1/+1`.

**Expected output:**

```
[0.0, 0.5, 0.7, 2.2]
```
