`class_weights(n, seed)` should return the weight from the lesson (total
pixels / (4 × the class's pixels)) for the four classes in the masks of
`make_scenes(n, size=32, seed=seed)`, rounded to 2 places, as a list.

**Expected output:**

```
[0.28, 5.87, 7.12, 12.0]
[0.28, 7.23, 6.33, 9.23]
```
