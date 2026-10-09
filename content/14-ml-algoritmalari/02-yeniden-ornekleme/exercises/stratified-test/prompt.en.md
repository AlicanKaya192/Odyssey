Write the function `stratified_test(y, test_size, seed)`:
`rng = np.random.default_rng(seed)`; in the order of `np.unique(y)`, shuffle each
class's indices with `rng.permutation` and take the first
`round(len * test_size)` into the test. It returns the test indices as a
**sorted** list.

**Expected output:**

```
[2, 4, 5, 7, 8]
```
