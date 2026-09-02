You will show change over time with a **line** rather than bars.

**What you need to do:**

1. The `months` and `sales` lists are ready in the starter code.
2. Draw a **line chart** with the months on x and the sales on y, marking the
   points with `marker="o"`.
3. Set the title to `Monthly sales`.
4. Label the y axis **with its unit**: `Sales (thousands)`.
5. Print, in order: the number of lines, the line's y data as a list, and the
   y label.

**Expected output:**

```
1
[120, 150, 130, 180]
Sales (thousands)
```

**You are learning two things:**

- **A bar compares categories, a line shows how something changed.** You
  could draw months as bars, but the trend reads better as a line.
  `marker="o"` marks the actual measurements — the line between them is a
  guess, the points are the data.
- **The y label carries a unit:** `Sales (thousands)`. Had you written only
  `Sales`, the reader would have had to guess whether it means items, pounds
  or thousands.
