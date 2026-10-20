Sorted bin edges (`edges`) are given; `n` edges make `n + 1` bins. Write the function `bin_shares(values, edges)`:

- Each value's bin is `bisect.bisect_left(edges, value)`: the number of edges smaller than the value. A value equal to an edge falls into the bin to the **left** of that edge.
- Return the share of values in each bin, rounded to three digits, in bin order.

**Expected output:**

```
[0.2, 0.4, 0.2, 0.2]
[0.25, 0.25, 0.25, 0.25]
```
