Write the function `integer_sqrt(n)` **with binary search on the answer**:
it returns the **largest** `k` with `k * k <= n` (`n >= 0`).

- `integer_sqrt(50)` → `7` (`7 * 7 = 49`, `8 * 8 = 64`)
- `integer_sqrt(0)` → `0`

**The idea:** the answer is between `0` and `n`. As `k` grows, `k * k <= n`
is true at first and then false for good. Try the middle of the range: if the
condition holds, the answer is this or something larger (`answer = mid`,
`lo = mid + 1`); if not, something smaller (`hi = mid - 1`).

**Rules:** do not use `math.sqrt`, `math.isqrt` or `** 0.5`.

**Expected output:**

```
0 0
1 1
15 3
16 4
50 7
99 9
1000000
```

Even for the huge number on the last line about 40 rounds are enough.
