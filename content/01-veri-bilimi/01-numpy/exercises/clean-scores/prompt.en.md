Cells are empty in real data. Two of these six scores are missing; you will
find them and fill them with the average.

**What you need to do:**

1. The `scores` array is ready in the starter code, with two `np.nan` in it.
2. Find how many values are missing and keep it in a variable called
   `missing`.
3. Compute the average **without counting** the missing ones, into a variable
   called `average`.
4. Take a **copy** of `scores` (call it `filled`) and fill the empty cells
   with that average.
5. Print, in order: `missing`, `average`, `filled`, and the mean of `filled`
   rounded to two places.

**Expected output:**

```
2
75.0
[80. 75. 90. 70. 75. 60.]
75.0
```

**There are two traps:**

- `scores.mean()` gives you `nan` — a single missing value ruins the whole
  result. You need `np.nanmean`.
- If you fill **without taking a copy** you corrupt the original. In NumPy an
  assignment and a slice touch the same data; `.copy()` is essential.

It is no coincidence that the last average matches `average`: filling the
gaps with the mean does not change the mean. This is a method deliberately
used in real data work.
