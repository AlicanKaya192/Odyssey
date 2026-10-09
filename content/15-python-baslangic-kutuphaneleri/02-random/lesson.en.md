# random

Rolling dice, picking a random element from a list, shuffling cards, drawing
a sample for an experiment, building a simulation... All of this is done with
the **`random`** module. In this section we see where random numbers really
come from, how to reproduce the same result (the **seed**), and the most used
functions.

## The seed: reproducing the same randomness

Random numbers on a computer are **pseudo-random**: they are produced by a
fixed calculation from a starting number (the seed). Start with the same seed
and you get the same sequence.

```python
import random

random.seed(42)
x = random.random()
die = random.randint(1, 6)
y = random.uniform(10, 20)
print(round(x, 4), die, round(y, 2))
random.seed(42)
print(round(random.random(), 4))
```

```text
0.6394 1 17.42
0.6394
```

`random()` gives a decimal between 0 and 1, `randint(1, 6)` an integer
between 1 and 6 (both included), `uniform(10, 20)` a decimal in the range.
Setting the seed to 42 again gives 0.6394 again as the first number. This
makes experiments and tests **reproducible**: when you find a bug, you can
rebuild the same situation with the same seed.

## Your own generator: random.Random

`random.seed` sets the single generator the whole program shares; if another
function calls `random` in between, your sequence shifts. Building a separate
generator for your own work is safer:

```python
import random

r = random.Random(7)
colors = ["red", "green", "blue"]
print(r.choice(colors))
print(r.choices(colors, k=5))
print(r.sample(range(1, 50), 6))
deck = list(range(1, 11))
r.shuffle(deck)
print(deck)
```

```text
green
['blue', 'green', 'red', 'blue', 'red']
[38, 4, 33, 14, 3, 6]
[9, 3, 6, 4, 5, 1, 8, 2, 10, 7]
```

- `choice` picks a single element.
- `choices(k=5)` makes five picks **with replacement**: the same element can
  come again.
- `sample(…, 6)` picks six different elements **without replacement** (like a
  lottery).
- `shuffle` shuffles the list **in place** and returns `None`; the original
  order is lost.

## Weighted choice

```python
import random

r = random.Random(7)
counts = {"red": 0, "green": 0, "blue": 0}
for c in r.choices(["red", "green", "blue"], weights=[70, 20, 10], k=10000):
    counts[c] += 1
print(counts)
```

```text
{'red': 6992, 'green': 2012, 'blue': 996}
```

`weights` gives each option's share of probability: with weights 70/20/10,
red came 6992 times in 10,000 picks, very close to the expected 7000. The
weights do not need to add up to 100; their ratios matter.

## Distributions and the law of large numbers

```python
import random
import statistics as st

r = random.Random(1)
heights = [r.gauss(170, 10) for _ in range(10000)]
print(round(st.mean(heights), 2), round(st.stdev(heights), 2))
r = random.Random(3)
print(sum(r.randint(1, 6) == 6 for _ in range(60000)))
```

```text
170.03 9.92
9915
```

`gauss(170, 10)` draws from a normal distribution with mean 170 and standard
deviation 10; the 10,000 numbers had a mean of 170.03 and a standard
deviation of 9.92. In 60,000 dice rolls a six came 9915 times; the expected
number is 10,000. As the number of trials grows, the share approaches the
expected value: the **law of large numbers**.

## Common mistakes

```python
import random

a = random.Random(5)
b = random.Random(5)
print([a.randint(1, 100) for _ in range(3)], [b.randint(1, 100) for _ in range(3)])
try:
    random.Random(1).sample([1, 2, 3], 5)
except ValueError as error:
    print("ValueError:", error)
```

```text
[80, 33, 95] [80, 33, 95]
ValueError: Sample larger than population or is negative
```

Two generators with the same seed give the same sequence; if you want "two
different random sequences", give different seeds. `sample` raises an error
when asked for more elements than the population has; if you need to choose
with replacement, use `choices`.

**`random` is not for security.** Anyone who knows the seed can predict the
sequence. Passwords, tokens and verification codes are generated with the
`secrets` module (in the advanced Python module).

## Summary

- Random numbers are produced from a seed; the same seed gives the same
  sequence.
- For your own work, build a separate generator with `random.Random(seed)`.
- `random`, `randint`, `uniform`; `choice`, `choices` (with replacement,
  `weights`), `sample` (without replacement), `shuffle` (in place).
- `gauss` is the normal distribution; with more trials shares approach the
  expected values.
- Where security matters, use `secrets`, not `random`.
