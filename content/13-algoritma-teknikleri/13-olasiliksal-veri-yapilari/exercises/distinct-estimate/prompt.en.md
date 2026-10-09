Write the function `distinct_estimate(items, p)` with **HyperLogLog**.
`m = 2 ** p` buckets. For each item `v = h(item, 0)`; the bucket is
`v & (m - 1)`; `rest = v >> p`; the rank is
`rank = (64 - p) - rest.bit_length() + 1`; a bucket's value is the largest
`rank` so far.

Once the buckets are filled, the estimate formula is ready in the starter
code.

**Expected output:**

```
100 108
5000 4949
40000 36206
```
