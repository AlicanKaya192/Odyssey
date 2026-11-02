## The SRM test, for any split

If the expected split is not 50/50 it is given with `f_exp`:

```python
from scipy import stats


def srm_p(n_a, n_b, share_b=0.5):
    total = n_a + n_b
    expected = [total * (1 - share_b), total * share_b]
    return stats.chisquare([n_a, n_b], f_exp=expected).pvalue


print(f"{srm_p(24976, 23973):.1e}")
print(f"{srm_p(9030, 970, share_b=0.1):.3f}")
```

```text
5.8e-06
0.317
```

The second line is a 90/10 test: 970 people in B, 1000 expected. That
difference can be explained by chance.

## When SRM is seen

1. Do not read the result; hold the decision.
2. Look segment by segment: platform, browser, country, day, new /
   returning user.
3. Compare the logging paths: do both groups go through the same event
   code?
4. Look at redirects, caching, the bot filter and crash logs.
5. Once the cause is fixed, start the test **from scratch**; do not merge
   with the old data.

## When to run an A/A test?

- When a new experiment system is set up.
- When the assignment, logging or analysis code changes.
- Continuously: some teams always run an A/A test on a small part of the
  traffic.
