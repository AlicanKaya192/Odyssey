`stacked_tops(names, a, b)` should **stack** the two series: the second
starts from the top of the first (`bottom=a`). Close the figure and return
the **top** heights of the second series' bars (`p.get_y() +
p.get_height()`) as a list; these are the `a + b` totals. In the starter code
the second series starts from zero.

**Expected output:**

```
[175.0, 230.0, 115.0]
```
