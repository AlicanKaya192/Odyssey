Let the real data be the standard normal and the generator a normal
distribution with mean `mu_g` and standard deviation `sd_g`.
`optimal_d(xs, mu_g, sd_g)` should return the best discriminator's value for
every `x`: `p_data(x) / (p_data(x) + p_g(x))`. The normal density is
`exp(-(x - m) ** 2 / (2 * s ** 2)) / (s * sqrt(2 * pi))`. The result is a
list of `float`s rounded to 3 places.

**Expected output:**

```
[0.5, 0.5, 0.5]
[0.881, 0.5, 0.119]
```
