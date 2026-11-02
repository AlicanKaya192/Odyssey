In the layout test with 80 people each (`make_layout_test(n=80, seed=181)`)
first print each layout's mean as a dictionary (ready), then print F (3
places) and p (4 places) on one line with `stats.f_oneway`.

**Expected output:**

```text
{'A': 7.97, 'B': 8.38, 'C': 9.17, 'D': 8.58}
2.427 0.0655
```
