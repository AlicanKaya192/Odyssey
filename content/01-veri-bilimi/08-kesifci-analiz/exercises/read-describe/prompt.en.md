`describe()` gives you a table; in this exercise you will **draw meaning**
out of it.

**What you need to do:**

1. Print the mean of the `score` column, rounded to two decimals.
2. Print its median.
3. Print its standard deviation, rounded to two decimals.
4. Print **whether the mean is below the median** (`True`/`False`).

**Expected output:**

```
72.8
76.0
16.51
True
```

**The last line is the real question.** If the mean is below the median the
distribution is **left-skewed**: a few low values at the bottom are dragging
the mean down. That is the case here — the scores of 45 and 51 pull it
down.

Were it the other way round (the mean above the median) there would be a few
high values at the top; that is almost always what income data looks like.

**The standard deviation** tells you the spread: 16.5 means the scores are
quite widely scattered around the mean. Had it been small, everyone would
look alike.
