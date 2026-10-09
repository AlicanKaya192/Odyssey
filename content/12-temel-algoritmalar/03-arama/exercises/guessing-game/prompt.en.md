Someone picked a number between 1 and `n`. After each guess they tell you
"higher", "lower" or "got it". The best strategy is to say the **middle** of
the remaining range every time.

Write the function `count_guesses(n, secret)`: it returns how many guesses
this strategy needs to find `secret`. The guess is `(lo + hi) // 2`; the
range starts at `lo = 1`, `hi = n`.

Then print the worst case for 100 and 1 000 000: the largest number of
guesses over **every** `secret` in the range. (Trying every number for
1 000 000 takes long; instead try only `secret = 1` and `secret = n` and take
the larger.)

**Expected output:**

```
100 7
1000000 20
```

At most 7 guesses for 100 numbers, 20 for a million: `O(log n)`.
