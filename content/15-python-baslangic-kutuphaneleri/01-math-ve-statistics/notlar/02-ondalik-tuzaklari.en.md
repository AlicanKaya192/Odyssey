Five traps you will meet when working with decimal numbers (floats), all
measured on this computer:

```python
import math

print(math.isclose(1e-10, 0), math.isclose(1e-10, 0, abs_tol=1e-9))
print(1e16 + 1 == 1e16, 10 ** 16 + 1 == 10 ** 16)
print(7 / 2, 7 // 2, -7 // 2, 7 % 3, -7 % 3)
print(0.1 * 3, float("inf") - float("inf"))
```

```text
False True
True False
3.5 3 -4 1 2
0.30000000000000004 nan
```

1. **Comparing near zero.** By default `isclose` uses a **relative**
   tolerance (in proportion to the size of the numbers); when comparing with
   zero the relative tolerance is zero and `1e-10` does not count as "close to
   zero". For closeness to zero, pass `abs_tol`.
2. **Large floats run out of precision.** `1e16 + 1` is still `1e16`: a float
   holds about 15–16 digits. Integers (`int`) are unlimited; `10 ** 16 + 1` is
   computed correctly. If you need exactness, work with integers.
3. **Kinds of division.** `/` always gives a float (3.5). `//` rounds down,
   not towards zero: `-7 // 2` is **−4**. `%` follows it: `-7 % 3` is **2**.
4. **The number shown is not the number stored.** `0.1 * 3` prints as
   `0.30000000000000004`; use `round` or formatting (`f"{x:.2f}"`) when
   printing amounts, not in the calculation.
5. **`inf - inf` is not a number** (`nan`). `nan` silently spreads through
   calculations; if a result turns out an unexpected `nan`, search backwards
   with `math.isnan`.

Exact decimals (money) with `decimal` and fractions with `fractions` are in
the advanced Python module.
