Write what `train_test_split` does yourself: `split(items, test_share, seed)`.

- Take a **copy** of the `items` list; don't change the original list.
- Shuffle the copy with a generator you build with `random.Random(seed)` (`shuffle`).
- The number of test items is `round(len(items) * test_share)`.
- The **first** that many items of the shuffled list are the test set, the rest is the training set.
- Return `(train, test)`.

The same seed should give the same split every time.

**Expected output:**

```
test: ['C7', 'C9', 'C10']
again: ['C7', 'C9', 'C10']
other seed: ['C6', 'C10', 'C4']
original: ['C1', 'C2', 'C3']
```
