Measure what happens when a single `shift` is forgotten.

The correct table (`table`) is ready in the starter code.

**What to do:**

1. Fit a linear regression on the correct table (training up to the end of
   2023) and print the 2024 test error with two decimals.
2. Build a faulty table: in a copy of `table` replace the `mean7` column with
   `s.rolling(7).mean()` (no shift; align with `.reindex(table.index)`). Fit
   the same model and print its test error.
3. Print the correlation between `mean7` and the target (`y`) in the two
   tables with three decimals on one line (the correct table first).
4. Print the coefficient of `mean7` in the faulty model and its counterpart in
   the correct model with two decimals on one line (the correct model first).
5. Which days does the faulty feature cover on 10 March 2024? Print that value
   and the mean of the sales of 4–10 March with one decimal on one line.

**Expected output:**

```
11.51
10.55
0.662 0.671
0.14 1.19
282.6 282.6
```

The error "improved" and no warning appeared. But the faulty `mean7` includes
10 March itself (4–10 March); its correlation with the target rose and the
model leant on it more. In real use you cannot compute that average without
knowing the sales of 10 March; this result can never be repeated.
