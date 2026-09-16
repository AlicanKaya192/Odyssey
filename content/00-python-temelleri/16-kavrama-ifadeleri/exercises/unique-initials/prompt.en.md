You will produce a set with no repeats.

The data you have:

```python
words = ["Ada", "alan", "Grace", "ada", "Gauss"]
```

**What to do:**

1. `initials` — the first letters of the words in **lower case**, as a set
   (no repeats).
2. `unique` — the words themselves in lower case, as a set.
3. Print both through `sorted()`, because a set has no guaranteed order.

**Expected output:**

```
['a', 'g']
['ada', 'alan', 'gauss', 'grace']
```

> `sorted(initials)` turns the set into a sorted list; you still write the
> set comprehension yourself.
