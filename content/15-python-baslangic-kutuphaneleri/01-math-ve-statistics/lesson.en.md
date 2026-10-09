# math and statistics

Everything a calculator can do is in Python: `+`, `-`, `*`, `/`, `**`. For
square roots, logarithms, combinations or the greatest common divisor you use
the **`math`** module; for statistics such as the mean, median, standard
deviation or correlation, the **`statistics`** module. Both are in the
standard library and make NumPy unnecessary for small data. In this section
we first see a trap of decimal numbers, then the most used functions of the
two modules.

## Decimal numbers are not exact

The computer stores decimal numbers in binary; numbers like `0.1` cannot be
written exactly, and small errors add up.

```python
import math

print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
total = 0.0
for value in [0.1] * 10:
    total += value
print(total, sum([0.1] * 10), math.fsum([0.1] * 10))
```

```text
0.30000000000000004 False
True
0.9999999999999999 1.0 1.0
```

`0.1 + 0.2` is not exactly `0.3`; that is why decimal numbers are compared not
with `==` but with **`math.isclose`**. Adding `0.1` ten times in a loop gives
`0.9999999999999999`: every addition adds a small error. `math.fsum`
compensates for the errors and finds exactly `1.0`; since Python 3.12 the
built-in `sum()` does the same compensation for floats. If you accumulate in
your own loop, the error grows.

## Rounding

```python
import math

print(math.floor(-2.5), math.ceil(-2.5), math.trunc(-2.5))
print(round(2.5), round(3.5), round(2.675, 2))
```

```text
-3 -2 -2
2 4 2.67
```

`floor` rounds down (−3), `ceil` up (−2), `trunc` towards zero (−2); the
difference shows with negative numbers. The built-in `round` does **banker's
rounding**: exactly at the half it goes to the nearest **even** number, so
`round(2.5)` is 2 and `round(3.5)` is 4. `round(2.675, 2)` is 2.67, not 2.68:
`2.675` is stored slightly smaller in binary. Where exact rounding matters,
such as money, the `decimal` module is used (in the advanced Python module).

## Integer arithmetic

```python
import math

print(math.prod([1, 2, 3, 4]), math.factorial(5))
print(math.comb(10, 3), math.perm(10, 3))
print(math.gcd(24, 36), math.lcm(4, 6), math.isqrt(17))
```

```text
24 120
120 720
12 12 4
```

`prod` is the product, `factorial` the factorial. `comb(10, 3)` is the number
of ways to choose a **group** of three from ten people (120), `perm(10, 3)`
the number of arrangements where order matters (720). `gcd` is the greatest
common divisor, `lcm` the least common multiple. `isqrt` is the integer square
root (the whole part of the square root of 17 is 4); for big numbers it is
more reliable than `int(math.sqrt(n))` because it never goes through a
decimal.

## Logarithms, exponents, distances and special values

```python
import math

print(math.log(100, 10), math.log10(1000), math.log2(1024))
print(round(math.exp(1), 6), math.hypot(3, 4), math.dist((0, 0), (3, 4)))
print(math.inf > 10 ** 100, math.isnan(math.nan), math.nan == math.nan)
```

```text
2.0 3.0 10.0
2.718282 5.0 5.0
True True False
```

`log(x, base)` works in any base, `log10` and `log2` are short forms; `log(x)`
without a base is the natural logarithm (base e). `hypot` is the hypotenuse
of a right triangle, `dist` the distance between two points. `math.inf` means
no number is larger; `math.nan` is "not a number" and is **not even equal to
itself**: whether a value is `nan` is checked with `math.isnan`.

## statistics: location and spread

```python
import statistics as st

data = [2, 4, 4, 4, 5, 5, 7, 9]
print(st.mean(data), st.median(data), st.mode(data))
print(st.multimode([1, 1, 2, 2, 3]))
print(st.pstdev(data), round(st.stdev(data), 4))
print(st.quantiles(data, n=4))
```

```text
5 4.5 4
[1, 2]
2.0 2.1381
[4.0, 4.5, 6.5]
```

The mean is 5, the median 4.5 (with an even number of values, the mean of the
middle two), the most frequent value 4. If there are several most frequent
values, `multimode` gives them all. There are two standard deviations:
**`pstdev`** treats the data as the whole population and divides by `n` (2.0);
**`stdev`** treats the data as a **sample** and divides by `n − 1` (2.1381).
If your data is a part taken from a larger group, use `stdev`.
`quantiles(n=4)` gives the three cut points that split the data into four
equal parts: the quartiles (4.0, 4.5, 6.5).

## Relationship and distribution

```python
import statistics as st

x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
print(round(st.correlation(x, y), 4))
print(st.linear_regression(x, y))
iq = st.NormalDist(mu=100, sigma=15)
print(round(iq.cdf(130), 4), round(iq.inv_cdf(0.975), 2))
```

```text
0.7746
LinearRegression(slope=0.6, intercept=2.2)
0.9772 129.4
```

`correlation` is the Pearson correlation (0.7746: a strong, positive
relationship). `linear_regression` gives the slope and intercept of the
least-squares line: `y ≈ 0.6 x + 2.2`. `NormalDist` is a normal distribution
object: in a distribution with mean 100 and standard deviation 15, the
probability of staying below 130 is 97.72% (`cdf`), and the value separating
the lowest 97.5% is 129.4 (`inv_cdf`).

## Summary

- Compare decimal numbers with `math.isclose`; for long sums use `math.fsum`
  or `sum` (accumulating with `+=` in your own loop adds up errors).
- `floor`, `ceil`, `trunc`; `round` does banker's rounding.
- `prod`, `factorial`, `comb`, `perm`, `gcd`, `lcm`, `isqrt`; `log`, `exp`,
  `hypot`, `dist`; `inf` and `nan` (`isnan`).
- `statistics`: `mean`, `median`, `mode`, `multimode`, `stdev` (sample) and
  `pstdev` (population), `quantiles`, `correlation`, `linear_regression`,
  `NormalDist`.
