Find the **middle** of three numbers, the one that is neither the largest
nor the smallest, and put it in the variable `middle`:

```python
a = 17
b = 42
c = 29
```

```
29
```

Rule: `sorted`, `min` and `max` are not allowed. Only `if`, comparisons
and `and` / `or`.

What does it mean for a number to be in the middle? It is greater than or
equal to one of the others and smaller than or equal to the other. For
`a` there are two ways: `b <= a <= c` or `c <= a <= b`. Build the same
idea for `b` and `c`.

> Watch out: your code must work for any order, not just these three
> numbers. When you are done, change the values and try (for example
> `a = 42`, `b = 29`, `c = 17`; you should still get `29`), then put them
> back.
