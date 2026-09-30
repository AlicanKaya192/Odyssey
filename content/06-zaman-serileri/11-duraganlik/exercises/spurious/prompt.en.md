`two_walks.csv` holds two random walks produced **independently** of each
other (`date`, `a`, `b`; 500 business days). There is no link between them.
Try to see that from the data.

**What to do:**

1. Read the file as a table `w` with a date index.
2. Print the correlation of the **levels** of `a` and `b`, rounded to three
   decimals.
3. Print the correlation of their **changes** (`w.diff()`), rounded to three
   decimals.
4. How much does the correlation of the levels move from period to period?
   Split the series into five pieces of 100 days (`w.iloc[0:100]`,
   `w.iloc[100:200]`, ...) and print the level correlation in each piece,
   rounded to two decimals, as a list.
5. Print the correlation of the changes for the same five pieces as a list
   with two decimals.

**Expected output:**

```
0.907
0.001
[-0.3, 0.54, 0.79, 0.34, -0.45]
[-0.15, -0.01, 0.01, 0.1, 0.05]
```

The correlation of the levels is around 0.9 over the whole series; but piece
by piece it swings between large positives and large negatives. A real
relationship does not behave like that. The correlation of the changes is near
zero in every piece: there is no link between the two series.
