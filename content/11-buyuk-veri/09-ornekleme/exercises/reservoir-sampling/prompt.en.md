Write reservoir sampling yourself and check that it gives every item an
equal chance.

**What to do:**

1. Write the function `reservoir(items, k, seed)`:
   - `rng = random.Random(seed)`,
   - put the first `k` items in a list,
   - for every later `i`-th item, `j = rng.randint(0, i)`; if `j < k`,
     `sample[j] = item`,
   - return the list.
2. Print the result of `reservoir(range(1, 100_001), 5, seed=7)` sorted.
3. An equality check: `seed` from 0 to 999, each time
   `reservoir(range(100), 5, seed)`. Of the chosen items, how many are in the
   lower half (`< 50`) and how many in the upper half; print the two numbers
   on one line.

**Expected output:**

```
[3302, 26216, 31671, 61488, 88915]
2467 2533
```

The two halves are almost equal: no item is favoured.
