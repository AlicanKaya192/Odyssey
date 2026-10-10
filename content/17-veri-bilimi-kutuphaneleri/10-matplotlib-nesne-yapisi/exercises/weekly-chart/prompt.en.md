`weekly_chart(values)` should open a figure with `fig, ax = plt.subplots()`,
plot the values against weeks (`1, 2, ..., n`), set the title to `"Weekly
sales"`, the x label to `"week"`, the y label to `"sales"`, and save it as
`weekly.png`. Then close the figure and return `[title, x label, y label,
number of lines]`. In the starter code the labels are missing and the figure
is not closed.

**Expected output:**

```
['Weekly sales', 'week', 'sales', 1]
```
