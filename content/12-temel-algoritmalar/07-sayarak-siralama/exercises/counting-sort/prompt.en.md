Write the function `counting_sort(items, max_value)`: it sorts a list of
integers between `0` and `max_value` by counting.

1. Build a counter list of length `max_value + 1`.
2. Increase each element's counter by one.
3. Walk the counters in order; add each value to the result as many times as
   it was counted.

Do not use `sorted` or `.sort()`.

**Expected output:**

```
[0, 1, 1, 3, 4, 4, 4]
[]
```
