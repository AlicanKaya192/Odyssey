Given the softmax output `a` and the derivative `da` arriving at the output,
`softmax_backward(a, da)` should return the derivative going to the scores:
`a_i · (da_i − a · da)` for every element (`a · da` is the dot product), 4
places. These derivatives always sum to zero.

**Expected output:**

```
[0.35, -0.09, -0.26]
True
```
