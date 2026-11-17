`scene_summary(n, seed)` should collect all boxes of `make_scenes(n, size=32,
seed=seed)` and return `[number of objects, objects per class (0, 1, 2),
mean box area (1 place)]`. The area is `(x2 - x1) * (y2 - y1)`.

**Expected output:**

```
[197, [72, 66, 59], 72.0]
[96, [27, 33, 36], 74.1]
```
