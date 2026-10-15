**Why it matters**

With `n` flaky tests that each pass 98%, the chance of a green pipeline
is `0.98 ** n`: 98% with 1 test, 90% with 5, 67% with 20.

**Source, symptom, fix**

| Source | Symptom | Fix |
|---|---|---|
| Order dependence | Passes alone, fails together | A fixture gives every test its own data |
| Time | Fails at the weekend, month end, midnight | Pass the clock as a parameter |
| Randomness | A different value every time | `random.Random(42)` |
| Set order | Changes from computer to computer | `sorted(...)` or compare sets |
| Waiting | Fails on a slow machine | Wait for the condition (limited retries) |
| Network | Fails when the internet is slow | A fake server, a recorded answer |
| Decimal numbers | `0.1 + 0.2 == 0.3` is false | `pytest.approx` |

**Fix patterns**

```python
import random
from datetime import datetime


def pick(items, rng):
    return rng.choice(items)


def is_weekend(now=None):
    now = now or datetime.now()
    return now.weekday() >= 5


print(pick(["a", "b", "c"], random.Random(42)))
print(is_weekend(datetime(2026, 10, 17)))
print(sorted({"web", "api", "db"}))
```

- The function **takes** both the random generator and the clock from
  outside; the test gives fixed values.
- `sorted` instead of turning a set into a list and relying on its order.

**Finding a flaky test**

- A test that both passes and fails on the same commit is flaky.
- Run the suspect test alone and with the whole file; if the results
  differ, it is order dependence.
- Catching a test that rarely fails takes many runs: to see a test that
  fails 2% of the time fail at least once with 95% probability takes 149
  runs.
