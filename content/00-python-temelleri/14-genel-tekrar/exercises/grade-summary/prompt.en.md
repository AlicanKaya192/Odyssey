You will use loops, conditions and functions together.

**What you need to do:**

1. Write a function called `summarise`. It takes a list of numbers and returns
   **three values**: how many passed, how many failed, and the average (floor
   division). The pass mark is **50**.

2. Call it with this list and print the three results on separate lines:

```python
[90, 40, 75, 30, 65]
```

**Expected output:**

```
3
2
60
```

The average: `(90 + 40 + 75 + 30 + 65) // 5 = 60`

> A function can return more than one value: `return passed, failed, average`.
> The caller takes all three at once.
