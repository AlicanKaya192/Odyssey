Write the function `halving_steps(n)`: while `n` is greater than 1 it halves
`n` with integer division (`n //= 2`) and returns how many times it halved.
If `n` is 1, it returns `0`.

Do not use `math.log`; the point is to see the logarithm with a loop.

Then print `n` and the result for 1, 2, 8, 1000 and 1 000 000.

**Expected output:**

```
1 0
2 1
8 3
1000 9
1000000 19
```

Only 19 steps for a million: `O(log n)`.
