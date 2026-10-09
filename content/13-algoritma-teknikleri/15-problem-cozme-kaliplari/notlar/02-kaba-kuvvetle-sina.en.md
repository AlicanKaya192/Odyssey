When you write a fast algorithm, how can you be sure it is right? A few
hand-picked examples can miss a subtle bug. The reliable way is **stress
testing**: write a slow but clearly correct brute-force solution, then race
the two solutions on hundreds of **small, random** inputs. The first difference
is the simplest example showing the bug.

```python
import random


def slow(temps):
    result = [0] * len(temps)
    for i in range(len(temps)):
        for j in range(i + 1, len(temps)):
            if temps[j] > temps[i]:
                result[i] = j - i
                break
    return result


def fast_buggy(temps):
    result, stack = [0] * len(temps), []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] <= t:   # bug: should not be <=
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result


def fast(temps):
    result, stack = [0] * len(temps), []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result


def stress(fn, trials=500):
    rng = random.Random(1)
    for _ in range(trials):
        temps = [rng.randint(15, 20) for _ in range(rng.randint(1, 8))]
        if fn(temps) != slow(temps):
            return temps, fn(temps), slow(temps)
    return "ok"


print(stress(fast_buggy))
print(stress(fast))
```

```text
([18, 18], [1, 0], [0, 0])
ok
```

The buggy version said "an equal temperature counts as warmer too"; the stress
test caught it with a two-item example: `[18, 18]`. The correct version agrees
with brute force on all 500 trials.

Two tips: keep the inputs **small** (so a failure can be traced by hand) and
pick values from a **narrow** range (temperatures between 15 and 20 produce
ties often; ties are where bugs often hide). Seed the random generator so the
failure repeats with the same example on every run.
