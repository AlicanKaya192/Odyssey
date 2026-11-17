`prepare(pixels)` should get `uint8` pixel values (0–255) ready for the
network with a `v2.Compose` chain: `v2.ToDtype(torch.float32, scale=True)`,
then `v2.Normalize([0.5], [0.25])`. Make the pixels a `uint8` tensor of shape
`(1, 1, n)`; return the result as a flat list rounded to 3 places.

**Expected output:**

```
[-2.0, -0.996, 0.008, 2.0]
```
