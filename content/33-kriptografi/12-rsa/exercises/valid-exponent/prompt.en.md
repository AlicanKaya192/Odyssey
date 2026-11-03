`valid_exponent(e, phi)` should return `True` if `e` is a valid public
exponent: `1 < e < phi` and `gcd(e, phi) == 1`. The starter code only
checks that `e` is odd; 15 is odd, but its gcd with 3120 is 15 and it has no
inverse.

**Expected output:**

```
True
False
False
```
