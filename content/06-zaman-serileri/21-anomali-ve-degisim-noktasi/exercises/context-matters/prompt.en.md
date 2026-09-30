Find the 12 events of the maintenance log in the pump pressure: first with a
z-score over the whole series, then with the deviation from the hour's median.

In the starter code `p` (the pressure), `events` (the event hours) and `calm`
(the series without the last week) are ready.

**What to do:**

1. Compute the z-score on `calm`. Print the hours whose absolute value passes
   3 as a `"%m-%d %H"` list and how many of them are in `events`, on one line.
2. For 03:00 on 5 September print the value, the z-score (one decimal) and the
   median of that hour (03:00) within `calm`, on one line.
3. Build a profile from the median of each hour
   (`calm.groupby(calm.index.hour).median()`), compute the residual and the
   robust score: `0.6745 * (residual - median) / MAD`.
4. Print the number of hours whose score passes 3 in absolute value and how
   many of them are in `events`, on one line.
5. Print the days (`"%m-%d"`, unique, sorted) of the hours that are flagged
   but **not** in `events`, as a list.

**Expected output:**

```
['09-03 14'] 1
5.89 -0.2 5.22
20 12
['09-30']
```

The rule that looks at the whole series sees one of the 12 events; the rule
that knows the context of the hour sees them all. The value at 03:00 on 5
September sits right by the mean, yet it is 0.67 bar too high for that hour.
The eight flags that are not in the log are all on the same day: something
else happened that day (in the lesson: the stuck sensor).
