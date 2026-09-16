You will print how many exercises are solved, along with the percentage.

The data you have:

```python
solved = 24
total = 257
```

**What to do:**

1. `remaining` — how many exercises are left.
2. `rate` — the share that is solved (`solved / total`). **Do not multiply
   by a hundred**; the specifier does that itself.
3. Print the three lines below, with percentages to **one decimal place**.

**Expected output:**

```
Solved: 24 / 257
Rate: 9.3%
Remaining: 233 (90.7%)
```

> `f"{rate:.1%}"` multiplies by a hundred and adds the `%` sign. Writing
> `rate * 100` makes the result a hundred times too big.
