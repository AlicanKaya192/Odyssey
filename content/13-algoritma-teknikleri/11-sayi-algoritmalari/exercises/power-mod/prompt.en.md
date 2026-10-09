Write the function `power_mod(base, exp, mod)` with **exponentiation by
squaring**: it returns the value of `base ** exp % mod`.

No `pow` and no `**`. If the exponent's last bit is 1, multiply the result by
the base; square the base; halve the exponent. `% mod` after every
multiplication.

**Expected output:**

```
24
64935414
1
```
