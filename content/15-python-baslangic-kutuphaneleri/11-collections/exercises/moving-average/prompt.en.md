Write the function `moving_average(values, window)`: add the values in
turn to a `deque(maxlen=window)` and, **after each addition**, put the
average of the values in the window into a list with `round(..., 2)`.
Before the window is full, the average of the values so far is taken.

**Expected output:**

```
[10.0, 15.0, 20.0, 30.0, 40.0]
[5.0, 5.0, 5.0]
```
