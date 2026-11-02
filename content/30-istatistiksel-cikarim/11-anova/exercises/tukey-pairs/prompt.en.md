In the layout test with 150 people each (`make_layout_test()`) print, one
per line in the form `A C`, the pairs with `p < 0.05` according to Tukey
HSD (pairs in `itertools.combinations` order). The starter code uses
uncorrected t-tests and finds an extra pair.

**Expected output:**

```text
A C
B C
```
