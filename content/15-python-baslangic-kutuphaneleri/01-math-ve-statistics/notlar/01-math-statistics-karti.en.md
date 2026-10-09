## math

| Function | What it does | Example |
|---|---|---|
| `isclose(a, b)` | compares decimals with a tolerance | `isclose(0.1 + 0.2, 0.3)` → `True` |
| `fsum(xs)` | error-free decimal sum | `fsum([0.1] * 10)` → `1.0` |
| `floor`, `ceil`, `trunc` | down, up, towards zero | `floor(-2.5)` → `-3` |
| `prod(xs)` | product | `prod([1, 2, 3, 4])` → `24` |
| `factorial(n)` | n! | `factorial(5)` → `120` |
| `comb(n, k)`, `perm(n, k)` | choosing, ordered arrangements | `comb(10, 3)` → `120` |
| `gcd`, `lcm` | common divisor, common multiple | `gcd(24, 36)` → `12` |
| `isqrt(n)` | integer square root | `isqrt(17)` → `4` |
| `log(x, b)`, `log2`, `log10`, `exp` | logarithms and exponent | `log2(1024)` → `10.0` |
| `hypot`, `dist` | hypotenuse, distance | `dist((0, 0), (3, 4))` → `5.0` |
| `pi`, `e`, `inf`, `nan`, `isnan` | constants | `nan == nan` → `False` |

## statistics

| Function | What it does |
|---|---|
| `mean`, `fmean` | mean (`fmean` always a float and faster) |
| `median`, `median_low`, `median_high` | median; lower/upper middle for an even count |
| `mode`, `multimode` | most frequent value(s) |
| `stdev`, `variance` | sample (`n − 1`) |
| `pstdev`, `pvariance` | population (`n`) |
| `quantiles(xs, n=4)` | cut points (quartiles) |
| `correlation(x, y)` | Pearson correlation |
| `linear_regression(x, y)` | slope and intercept |
| `NormalDist(mu, sigma)` | `cdf`, `inv_cdf`, `pdf`, `mean`, `stdev` |

## When NumPy?

`statistics` is plain Python: comfortable up to a few thousand values, slow
with millions. For large arrays and tables NumPy and pandas are used (the
Data Science Libraries module).
