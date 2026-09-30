`web_traffic.csv` holds a site's daily visits. There are a few unusual
days in it: see how they spoil the smoothing, then find them with a rolling
window.

**What to do:**

1. Read the file with a date index; take the `visits` column into a series
   called `visits`.
2. For 14 March 2024 print the 7-day rolling **mean** (rounded to a whole
   number) and the rolling **median** on one line.
3. Compare each day with its own past: `base = visits.shift(1).rolling(28)`
   and `z = (visits - base.mean()) / base.std()`.
4. Print the z value of 14 March 2024, rounded to one decimal.
5. Print the days whose absolute `z` is above 3 as a list in `"%m-%d"` form.
6. Print the z values of those days as a list rounded to one decimal.

**Expected output:**

```
4587 4090.0
11.2
['03-14', '06-20', '10-08']
[11.2, 8.9, -6.5]
```

A single spike day pulled the mean 500 visits above the median; the median
stayed put.
The z-score caught three days: two upwards (campaigns) and one downwards (an
outage). Without `shift(1)` the unusual day enters its own baseline and its
deviation looks small.
