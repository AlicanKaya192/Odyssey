Three side lengths are given:

```python
a = 3
b = 4
c = 8
```

Can they form a triangle, and if so, what kind? Put the answer in the
variable `kind` and print it:

- `"not a triangle"`: if they cannot
- `"equilateral"`: if all three sides are equal
- `"isosceles"`: if exactly two sides are equal
- `"scalene"`: if no sides are equal

```
not a triangle
```

For a triangle to exist, the sum of **any** two sides must be **greater**
than the third: `a + b > c`, `a + c > b` and `b + c > a`. If even one of
them fails, the sides do not meet.

> Watch out: none of these sides are equal, so `"scalene"` may come to
> mind first. But whether a triangle exists must be checked first; the
> **order** of the conditions changes the result.
