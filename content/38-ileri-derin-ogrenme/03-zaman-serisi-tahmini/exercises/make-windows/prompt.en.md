`make_windows(values, size)` should build window examples from a series: in
each example `size` consecutive values are the input and the value right
after them the target. Return a two-item list: the list of inputs and the
list of targets.

**Expected output:**

```
[[1, 2], [2, 3], [3, 4]]
[3, 4, 5]
```
