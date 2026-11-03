# Modular Arithmetic

All the tools so far were **symmetric**: the two sides shared the same key.
But how is that key shared the first time? How do two computers that have
never met reach a common secret over a line anyone can listen to? The
answer of the next sections (RSA, Diffie-Hellman) rests on a single area of
mathematics: **modular arithmetic**. This section builds that toolbox.

## Clock arithmetic

Five hours after 10 o'clock is not 15 but 3: on reaching 12 you start
again. This "wrapping around" arithmetic is called **mod**. `a mod n` is the
remainder of `a` divided by `n`; in Python, `%`.

```python
print((10 + 5) % 12)
print(27 % 12)
print((-3) % 12)
print((7 * 8) % 12)
```

```text
3
3
9
8
```

In Python the result is always between `0` and `n - 1`, even for a negative
number: 3 hours back from 0 is 9. Addition and multiplication work as usual
inside mod; you can take `% n` at every step if you like, and the result
does not change.

## Big powers: `pow(base, exp, mod)`

Cryptography computes `base ** exp % mod` with numbers hundreds of digits
long. Computing the power first and taking the remainder afterwards makes
needlessly huge numbers; the three-argument form of `pow` keeps every
intermediate result inside the mod.

```python
print(len(str(7 ** 128)))
print(7 ** 128 % 13)
print(pow(7, 128, 13))
```

```text
109
3
3
```

The two ways gave the same result, but the first built a 109-digit number.
When real exponents are hundreds of digits long, that way never finishes.
The idea `pow` uses is **square and multiply**: it looks at the binary
digits of the exponent, squares the base at each step, and multiplies it
into the result when the digit is 1.

```python
def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


print(mod_pow(7, 128, 13))
print(mod_pow(5, 117, 19) == pow(5, 117, 19))
print(bin(117))
```

```text
3
True
0b1110101
```

117 has seven binary digits: the loop ran only seven rounds. Even if the
exponent had a thousand digits, the number of rounds is the number of
binary digits; that is why the huge exponents of cryptography are computed
quickly.

## Greatest common divisor and inverse

There is no division inside mod; there is an **inverse** instead. The
inverse of `a` mod `n` is the number `x` with `a * x % n == 1`. An inverse
exists only if the **greatest common divisor** (gcd) of `a` and `n` is 1.

```python
import math

print(math.gcd(12, 18))
print(math.gcd(3, 11))
inverse = pow(3, -1, 11)
print(inverse, 3 * inverse % 11)
try:
    pow(4, -1, 8)
except ValueError as error:
    print("no inverse:", error)
```

```text
6
1
4 1
no inverse: base is not invertible for the given modulus
```

The inverse of 3 mod 11 is 4: `3 × 4 = 12`, which leaves 1 when divided by
11. Since 4 and 8 share the divisor 2, 4 has no inverse mod 8, and Python
says so with an error.

The classic way to find the inverse is the **extended Euclidean
algorithm**: it also finds the `x` and `y` with `a * x + b * y == gcd(a,
b)`. If the gcd is 1, `x` is exactly the inverse of `a`.

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


g, x, y = egcd(3, 11)
print(g, x, y)
print(3 * x + 11 * y)
print(x % 11)
```

```text
1 4 -1
1
4
```

`3 × 4 + 11 × (-1) = 1`: `x = 4` is the inverse itself. `x` is sometimes
negative; `x % 11` brings it between `0` and `10`. In the RSA section the
private key will be found exactly like this, as the inverse of a number.

## Fermat's little theorem

If `p` is prime and `a` is not divisible by `p`, then `a ** (p - 1) % p` is
always 1. This is the first sign of the order that appears when you work
mod a prime.

```python
print([pow(a, 6, 7) for a in range(1, 7)])
print([pow(a, 7, 8) for a in range(1, 8)])
```

```text
[1, 1, 1, 1, 1, 1]
[1, 0, 3, 0, 5, 0, 7]
```

7 is prime: every result is 1. 8 is not prime: the results are not 1. This
theorem explains why RSA decryption works; that is why primes are at the
heart of public-key cryptography.

## Summary

- `a % n` is the remainder of division; in Python the result is always
  between `0` and `n - 1`.
- `pow(base, exp, mod)` computes big powers with **square and multiply**,
  in as many steps as the exponent has binary digits.
- Inside mod there is an **inverse** instead of division; it exists only if
  the gcd is 1: `pow(a, -1, n)`.
- The **extended Euclidean algorithm** finds the inverse step by step.
- If `p` is prime, `a ** (p - 1) % p == 1` (Fermat); RSA rests on this.
