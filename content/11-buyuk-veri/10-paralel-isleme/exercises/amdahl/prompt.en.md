Write a function that works out the speed-up with Amdahl's law.

**What to do:**

Write the function `speedup(p, n)`:

- `p`: the share of the work that can be parallel (between 0 and 1),
- `n`: the number of cores,
- returns: `1 / ((1 - p) + p / n)`, rounded to **two decimals**.

Examples:

- `speedup(0.9, 4)` → `3.08`
- `speedup(0.9, 24)` → `7.27`
- `speedup(0.5, 4)` → `1.6`
