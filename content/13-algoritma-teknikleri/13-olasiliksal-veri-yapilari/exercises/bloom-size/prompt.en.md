Write the function `bloom_size(n, p)`: for `n` items and a false positive
rate `p` it returns the tuple `(m, k)`:

- `m = math.ceil(-n * math.log(p) / math.log(2) ** 2)`
- `k = round(m / n * math.log(2))`

**Expected output:**

```
(9585059, 7)
(143776, 10)
```
