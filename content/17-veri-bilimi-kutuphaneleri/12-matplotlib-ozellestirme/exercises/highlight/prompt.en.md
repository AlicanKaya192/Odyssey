`highlight(names, values, target)` should draw a horizontal bar chart: every bar
`"lightgray"`, only the bar named `target` `"tab:blue"`. Write the values at
the end of the bars (`ax.bar_label`) and remove the top and right frame
(`ax.spines[["top", "right"]].set_visible(False)`). Save it as `bars.png` and
close the figure. Return:

- `"colors"`: the bar colours, via `matplotlib.colors.to_hex`
- `"labels"`: the `bar_label` texts
- `"spines"`: the visibility of the top and right frame `[top, right]`

**Expected output:**

```
['#d3d3d3', '#d3d3d3', '#1f77b4']
['65', '95', '240'] [False, False]
```
