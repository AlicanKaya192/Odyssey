`percent_ticks(rates)` should draw rates stored between 0 and 1 as a line
chart and write the y axis labels as **percentages without decimals**
(`PercentFormatter(xmax=1, decimals=0)`). Draw the figure, return the first
**three** y tick labels and close the figure. The starter code uses
`xmax=100`: it writes 0.184 as something like `0.184%`.

**Expected output:**

```
['0%', '5%', '10%']
```
