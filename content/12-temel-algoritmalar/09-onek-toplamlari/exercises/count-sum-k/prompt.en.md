Write the function `count_sum_k(values, k)` **with a prefix sum + a
dictionary**: it returns the number of consecutive pieces adding up to
exactly `k`. The numbers can be negative.

1. Start the dictionary as `{0: 1}`.
2. At each element update the prefix sum; add `seen.get(total - k, 0)`
   pieces; then increase the counter of `total`.

**Speed requirement:** at the end of the code a list of 100 000 numbers is
counted; trying every piece would be 5 billion steps.

**Expected output:**

```
4
6
11656430
```
