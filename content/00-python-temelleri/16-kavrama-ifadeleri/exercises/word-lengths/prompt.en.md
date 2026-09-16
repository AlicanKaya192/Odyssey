You will build dictionaries with comprehensions.

The data you have:

```python
words = ["ada", "alan", "grace"]
scores = {"ada": 90, "alan": 45, "grace": 72}
```

**What to do — write all three with comprehensions:**

1. `lengths` — the length of every word (`{word: length}`).
2. `passed` — the entries in `scores` that are **50 or above**.
3. `flipped` — `scores` with its keys and values swapped.

Then print all three in order.

**Expected output:**

```
{'ada': 3, 'alan': 4, 'grace': 5}
{'ada': 90, 'grace': 72}
{90: 'ada', 45: 'alan', 72: 'grace'}
```

> To loop over a dictionary use `scores.items()`; it gives you two values
> on every pass.
