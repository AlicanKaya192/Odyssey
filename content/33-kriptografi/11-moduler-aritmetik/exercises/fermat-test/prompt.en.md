`passes_fermat(n, bases)` should return `True` if `pow(a, n - 1, n) ==
1` for **every** `a` in `bases`, and `False` if it fails for even one. The
starter code looks only at the first base. Note: the test only says
"probably prime"; `561 = 3 × 11 × 17` is not prime but passes with these
bases.

**Expected output:**

```
True
False
True
```
