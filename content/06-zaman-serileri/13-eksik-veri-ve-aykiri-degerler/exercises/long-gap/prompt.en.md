Delete the 14 days from 8 to 21 July from the clean 2024 sales and fill
them back in with two methods. In the starter code `truth` (the real values)
and `gap` (with the hole) are ready.

**What to do:**

1. Linear filling: `linear = gap.interpolate()`.
2. A weekly chain: `chain = gap.copy()`; go through the missing days **in
   date order** and write into each the value from 7 days earlier
   (`chain.loc[day - pd.Timedelta(days=7)]`).
3. Print the mean absolute error of the two methods within the gap, rounded to
   one decimal, on one line (linear first).
4. For the two Saturdays in the gap (13 and 20 July) print the true, linear
   and chain values, rounded to whole numbers, on two lines.
5. Print the standard deviation within the gap of the linear filling and of
   the chain, together with that of the truth, rounded to one decimal, on one
   line (order: truth, linear, chain).
6. Print how many `NaN` values remain after `gap.ffill(limit=3)`.

**Expected output:**

```
47.5 9.6
344 278 346
343 242 346
45.2 21.2 52.9
11
```

Linear filling misses both Saturday peaks and more than halves the variability
inside the gap: a straight, sloping line. The chain keeps the pattern. And `limit=3`
does not close the gap; it only fills its first three days.
