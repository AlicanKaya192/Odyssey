# Number Algorithms

Encryption, hash functions, random number generators and splitting big data
sets into parts all rest on the same few number ideas: the **greatest common
divisor**, **prime numbers**, **fast exponentiation** and **modular
arithmetic**. In this section we put the naive way and the fast way of each
side by side and compare them by counting steps.

## Greatest common divisor: Euclid

The naive way to find the greatest common divisor (gcd) of two numbers: try
every number downwards from the smaller one. **Euclid's algorithm** rests on a
single observation: if dividing `a` by `b` leaves the remainder `r`, then
`gcd(a, b) = gcd(b, r)`. The numbers shrink quickly at every step.

```python
import math


def gcd_slow(a, b):
    steps = 0
    for d in range(min(a, b), 0, -1):
        steps += 1
        if a % d == 0 and b % d == 0:
            return d, steps


def gcd_euclid(a, b):
    steps = 0
    while b:
        a, b = b, a % b
        steps += 1
    return a, steps


print(gcd_slow(1071, 462), gcd_euclid(1071, 462))
print(gcd_slow(832_040, 514_229), gcd_euclid(832_040, 514_229))
print(math.gcd(1071, 462))
```

```text
(21, 442) (21, 3)
(1, 514229) (1, 28)
21
```

The numbers on the second line are two consecutive Fibonacci numbers: they are
the **worst case** for Euclid, yet it takes 28 steps instead of half a million.
Euclid's number of steps is proportional to the number of digits of the
smaller number: `O(log min(a, b))`. The ready one in Python is `math.gcd`.

<figure class="fig"><div class="flow"><span class="node">gcd(1071, 462)</span><span class="arrow">→</span><span class="node">gcd(462, 147)</span><span class="arrow">→</span><span class="node">gcd(147, 21)</span><span class="arrow">→</span><span class="node">gcd(21, 0)</span><span class="arrow">→</span><span class="node ok">21</span></div><figcaption>1071 = 2 × 462 + 147, 462 = 3 × 147 + 21, 147 = 7 × 21 + 0. When the remainder is 0, the other number is the gcd.</figcaption></figure>

## Prime numbers: the sieve of Eratosthenes

To find out whether a number is prime, trying divisors up to its square root is
enough: if `36 = 4 × 9`, one of the divisors cannot exceed `√36 = 6`. But if
you want **all** the primes up to `n`, a **sieve** is faster than testing every
number separately: mark the multiples of each prime, and the unmarked ones are
prime.

```python
def primes_trial(n):
    found, checks = [], 0
    for x in range(2, n + 1):
        prime = True
        d = 2
        while d * d <= x:                  # only up to the square root
            checks += 1
            if x % d == 0:
                prime = False
                break
            d += 1
        if prime:
            found.append(x)
    return found, checks


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    marks = 0
    for p in range(2, math.isqrt(n) + 1):
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):   # multiples below p*p are marked
                is_prime[multiple] = False
                marks += 1
    return [x for x in range(n + 1) if is_prime[x]], marks


print(sieve(30)[0])
for n in (10_000, 100_000):
    t, s = primes_trial(n), sieve(n)
    print(n, len(s[0]), t[1], s[1])
```

```text
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
10000 1229 117527 16981
100000 9592 2745694 193078
```

Both ways find the same primes (9592 up to 100,000). Trial division made about
2.7 million divisions, the sieve about 193 thousand marks: roughly fourteen
times fewer. The sieve costs `O(n log log n)`, very close to `n` in practice.
The price is memory: a list of length `n + 1`.

## Fast exponentiation

Computing `3¹⁰⁰⁰⁰⁰⁰` does not need 999,999 multiplications. If the exponent is
even, `aᵉ = (a²)^(e/2)`; if odd, one `a` is set aside. The exponent halves at
every step: **exponentiation by squaring**. Taking `mod` at every step keeps the
numbers from growing too.

```python
def fast_pow(base, exp, mod):
    result, mults = 1, 0
    base %= mod
    while exp > 0:
        if exp % 2 == 1:                   # this bit of the exponent is 1
            result = result * base % mod
            mults += 1
        base = base * base % mod           # the square for the next bit
        mults += 1
        exp //= 2
    return result, mults


MOD = 1_000_000_007
print(fast_pow(3, 1_000_000, MOD))
print(pow(3, 1_000_000, MOD))
print(fast_pow(2, 10, 1000))
```

```text
(64935414, 27)
64935414
(24, 6)
```

27 multiplications instead of a million: `O(log e)`. Python's three-argument
`pow` gives the same result; the `pow(base, m - 1, mod)` in Rabin-Karp was
this. RSA encryption works with exponents hundreds of digits long thanks to
this method.

## Modular arithmetic

`a % m` is the remainder of dividing `a` by `m`, and the result is always
between `0` and `m − 1`. Addition and multiplication agree with mod:
`(a + b) % m = (a % m + b % m) % m`, and the same for multiplication. So taking
mod on intermediate results reaches the right result without dealing with huge
numbers. A large prime like `1_000_000_007` is a mod often used in hashing and
counting problems.

## In machine learning: the hashing trick

Opening a column for every word when turning text into numbers inflates memory
as the vocabulary grows. The **hashing trick** makes the `mod` of the word's
hash the column number: the number of columns stays fixed and no vocabulary is
kept. Since Python's `hash()` can change from run to run, a stable hash
(`zlib.crc32`) is used.

```python
import zlib


def hashed_counts(text, buckets):
    vector = [0] * buckets
    for word in text.lower().split():
        vector[zlib.crc32(word.encode()) % buckets] += 1
    return vector


print(hashed_counts("the cat sat on the mat", 8))
words = "the cat sat on mat".split()
print([zlib.crc32(w.encode()) % 8 for w in words])
```

```text
[3, 0, 1, 0, 0, 0, 2, 0]
[6, 0, 0, 0, 2]
```

Column 6 holds 2 because `the` occurs twice. But `cat`, `sat` and `on` fell into
the same column (0): a **collision**. More columns mean fewer collisions;
scikit-learn's `HashingVectorizer` uses 2²⁰ columns by default.

## Summary

- Euclid: `gcd(a, b) = gcd(b, a % b)`, `O(log min(a, b))`; the ready one is
  `math.gcd`.
- For primality, divisors up to the square root are enough; for all primes, a
  sieve.
- Fast exponentiation: `O(log e)` multiplications by halving the exponent;
  `pow(a, e, m)`.
- Modular arithmetic: taking mod on intermediate results does not change the
  result.
- The hashing trick: a fixed-size feature vector with `hash % columns`; watch
  out for collisions.
