Two of six daily temperature readings were never taken. First you will
**see** the gaps, then fill them.

**What you need to do:**

1. The `temps` Series is ready in the starter code, with two `None` in it.
2. Find how many readings are missing and keep it in `missing`.
3. Compute the mean and keep it in `average`.
4. Produce a new Series with the gaps filled by that mean, called `filled`.
5. Print, in order: `missing`, then `temps.count()` and `temps.size`
   **side by side**, the mean (rounded to two places), and `filled` as a
   list.

**Expected output:**

```
2
4 6
25.5
[21.0, 25.5, 24.0, 25.5, 27.0, 30.0]
```

**The real lesson is on the second line.** `count()` counts the filled cells
and `size` counts all of them; if they differ there are gaps in the data.

pandas skips missing values **by itself** when taking the mean — in NumPy you
got `nan` and had to say `nanmean`. It looks like a convenience, but it can
also stop you noticing how many records were empty. That is why you count
first.
