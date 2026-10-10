`annotate_peak(values)` should draw the values as a line chart (x = `0, 1, 2,
...`) and mark the **largest** value with an arrowed note reading `"peak"`
(`ax.annotate("peak", xy=(x, y), xytext=(x + 1, y), arrowprops=dict(arrowstyle="->"))`).
Save it as `peak.png` and close the figure. Return `[note_text, [x, y]]`:
the note's `xy` point (`int`). The starter code marks the last point.

**Expected output:**

```
['peak', [3, 310]]
```
