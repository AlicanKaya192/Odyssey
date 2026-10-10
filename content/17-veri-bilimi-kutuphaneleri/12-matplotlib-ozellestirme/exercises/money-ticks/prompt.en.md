`money_ticks(values)` should draw the values as a bar chart and write the y
axis labels with thousands separators and no decimals
(`StrMethodFormatter("{x:,.0f}")`). Draw the figure (`fig.canvas.draw()`),
return the **first three** y tick labels as a list, then close the
figure.

**Expected output:**

```
['0', '200,000', '400,000']
```
