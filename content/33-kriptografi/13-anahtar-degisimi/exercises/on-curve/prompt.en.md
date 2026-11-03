`on_curve(x, y, a, b, p)` should return `True` if the point `(x, y)` lies
on the curve `y² = x³ + a·x + b` (mod `p`). The starter code compares
without taking the mod; numbers that are equal mod `p` are not equal as
plain numbers.

**Expected output:**

```
True
True
False
```
