There are three rods: `"A"`, `"B"`, `"C"`. `"A"` holds `n` discs stacked from
largest to smallest. You must move them all to `"C"`; each move carries **one
disc**, and **a larger disc may not sit on a smaller one**.

The recursive solution has three steps:

1. Move the top `n − 1` discs to the spare rod (using the target as helper).
2. Move the largest disc to the target.
3. Move the `n − 1` discs from the spare onto the target, on top of the
   largest.

Write the function `hanoi(n, source, target, spare)`: it returns the moves as
a list of `(from, to)` tuples. If `n == 0`, an empty list.

**Expected output:**

```
A -> C
A -> B
C -> B
A -> C
B -> A
B -> C
A -> C
1023
```

10 discs take 1023 moves: `2ⁿ − 1`, exponential growth.
