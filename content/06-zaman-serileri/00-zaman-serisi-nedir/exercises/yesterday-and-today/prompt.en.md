Run the experiment from the lesson yourself: how closely are today's
sales linked to yesterday's, to the same day last week, and after shuffling?

The way to pair two sequences **shifted by one step** is slicing:

```python
values[:-1]   # all but the last:  "yesterday"
values[1:]    # all but the first: "today"
```

The two elements at the same position always form a (yesterday, today) pair.
For seven steps use `values[:-7]` and `values[7:]`.

**What to do:**

1. Take the `sales` column of `store_sales.csv` as a NumPy array
   (`.to_numpy()`).
2. Compute the today-yesterday correlation with `np.corrcoef(a, b)[0, 1]`.
3. Compute the correlation between today and 7 days earlier.
4. Shuffle the table with `sample(frac=1, random_state=42)` and compute the
   today-yesterday correlation on the shuffled `sales` array.
5. Print the three numbers rounded to three decimals, one per line.

**Expected output:**

```
0.695
0.958
0.018
```

The numbers are the same numbers; in the third one the only thing that
changed is the order. In a time series the information lives in the order.
