`miss_count(k, draws)` should draw `k` examples with
`random.Random(seed).sample(POOL, k)` for every seed from `0` to
`draws - 1` and count the draws in which at least one of the five
categories is missing. Return the count.

**Expected output:**

```
5 932
10 312
15 49
```
