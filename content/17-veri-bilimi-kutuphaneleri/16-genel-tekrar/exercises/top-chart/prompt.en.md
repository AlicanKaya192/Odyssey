`top_chart(channels, sales)` should compute total sales per channel (pandas
`groupby`), sort them **largest first** and draw a horizontal bar chart: the
largest bar `"tab:blue"`, the rest `"lightgray"`, values at the end of the
bars (`bar_label`). `barh` puts the first item at the bottom; to have the
largest on top, pass the sorted list **reversed**. Save it as `top.png` and
close the figure. Return:

- `"order"`: the channels from largest to smallest
- `"labels"`: the `bar_label` texts (in drawing order)
- `"highlight"`: the highlighted channel

**Expected output:**

```
['web', 'store', 'phone']
['2', '9', '10']
web
```
