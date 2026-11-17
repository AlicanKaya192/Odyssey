`same_size(img, kernel)` should apply an odd square kernel to the picture with
`F.conv2d`, choosing the padding so that the output is **the same size** as
the picture. The result is an integer nested list. The program prints each
pixel's neighbourhood sum with a 3 × 3 kernel of ones.

**Expected output:**

```
[1, 2, 2, 1]
[2, 4, 4, 2]
[2, 4, 4, 2]
[1, 2, 2, 1]
```
