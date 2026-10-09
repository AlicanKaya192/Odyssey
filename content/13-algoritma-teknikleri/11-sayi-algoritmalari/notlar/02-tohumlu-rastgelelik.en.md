A computer's "random" numbers actually come from a formula. One of the oldest
methods is the **linear congruential generator (LCG)**: the next number is
`(a × x + c) % m`. The starting value `x` is the **seed**.

```python
def lcg(seed, count, a=1103515245, c=12345, m=2**31):
    out, x = [], seed
    for _ in range(count):
        x = (a * x + c) % m
        out.append(x)
    return out


print([x % 100 for x in lcg(42, 6)])
print([x % 100 for x in lcg(42, 6)])
print([x % 100 for x in lcg(7, 6)])


def distinct_before_repeat(a, c, m, seed=1):
    seen, x = set(), seed
    while x not in seen:
        seen.add(x)
        x = (a * x + c) % m
    return len(seen)


print(distinct_before_repeat(5, 3, 16), distinct_before_repeat(4, 3, 16))
```

```text
[27, 64, 53, 6, 35, 32]
[27, 64, 53, 6, 35, 32]
[16, 33, 38, 71, 40, 21]
16 3
```

The same seed gives the same sequence: that is what writing `random_state=42`
means in machine learning, the experiment becomes repeatable. Since `m` is
limited, the sequence repeats one day; if `a` and `c` are chosen well
(`5, 3, 16`) it visits all 16 values, if chosen badly (`4, 3, 16`) it gets stuck
on three values.

Python's `random` module and NumPy's `default_rng` do not use an LCG but generators with much
longer cycles (Mersenne Twister, PCG64). The idea is the same, though: a seed +
modular arithmetic. Encryption needs the unpredictable `secrets` module.
