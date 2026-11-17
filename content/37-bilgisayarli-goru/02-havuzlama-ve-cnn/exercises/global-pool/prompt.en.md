`global_pool(fmap)` should return, for each channel of a feature map in
`(C, H, W)` order, the global mean and the global maximum
(`F.adaptive_avg_pool2d`, `F.adaptive_max_pool2d`, output size 1) rounded to
3 places, as two lists.

**Expected output:**

```
[2.5, 2.0]
[4.0, 8.0]
```
