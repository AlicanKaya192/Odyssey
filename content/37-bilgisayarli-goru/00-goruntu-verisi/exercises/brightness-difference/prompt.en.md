`brightness_difference(a, b)` should return the absolute difference of two
`uint8` pixel lists. The starter code subtracts in `uint8` and `10 − 30`
wraps around. Fix it by converting to `int16`, which can hold negative values,
before subtracting.

**Expected output:**

```
[20, 100, 0]
[255, 255]
```
