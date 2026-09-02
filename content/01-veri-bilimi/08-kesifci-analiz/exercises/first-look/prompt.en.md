You will write the first four checks you make when you open a new
dataset.

**What you need to do:**

1. Print the **shape** of the table.
2. Print the column **types** as a readable list.
3. Print the **total number of blank cells** in the table.
4. Print **how many distinct values** the `city` column has.

**Expected output:**

```
(10, 4)
['str', 'int64', 'int64', 'int64']
0
3
```

**Why these four:**

- **The shape** tells you the scale. Ten rows and a hundred thousand rows are
  different things.
- **The types** tell you whether cleaning is needed. If a numeric column
  shows up as `str` you cannot take an average.
- **The blanks** determine which results you can trust.
- **How many categories** there are: with 3 you can group, with 10,000 that
  column is an id column.

`sum()` is needed twice: the first counts per column, the second adds those
up.
