`convolve(img, kernel)` should take two nested lists (picture and kernel) and
compute the convolution without padding and with stride 1 (as in the
lesson, without flipping the kernel) using loops only. The output is an
`(H - kh + 1) x (W - kw + 1)` nested list. Do not use PyTorch.

**Expected output:**

```
[[-5, -5, -5], [-5, -5, -5]]
[[6, 9], [18, 21], [30, 33]]
```
