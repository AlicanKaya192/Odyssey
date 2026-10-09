Write the function `shuffled(items, seed)`: it returns a shuffled **copy** of
the list; the original must not change. The generator is
`rng = random.Random(seed)`.

Fisher-Yates: bring `i` down from the end to `1`; `j = rng.randint(0, i)` and
swap `i` and `j`. (For the same output the order and range must be exactly
this.) No `shuffle` and no `sample`.

**Expected output:**

```
[3, 4, 5, 1, 2]
[3, 2, 4, 5, 1]
['c', 'a', 'b']
```
