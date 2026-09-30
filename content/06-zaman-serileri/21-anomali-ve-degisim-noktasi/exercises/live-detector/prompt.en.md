Build a detector for the web traffic that uses only the past, and see what
changes depending on whether the expectation is built with the median or the
mean.

In the starter code `past` is ready: for each day, the values of the same
weekday over the last four weeks (four columns).

**What to do:**

1. Write the function `alarms(expected)`: it computes the relative deviation
   (`v / expected - 1`) and returns the days whose absolute value passes 0.25
   as a `"%m-%d"` list.
2. With the expectation `past.median(axis=1)` print the number of alarms and
   the list, one under the other.
3. With the expectation `past.mean(axis=1)` print the number of alarms.
4. Print as a list the days that alarm with the mean but **not** with the
   median.
5. For 21 March print the mean expectation, the median expectation and the
   actual value as whole numbers on one line.

**Expected output:**

```
12
['03-14', '06-20', '09-02', '09-03', '09-05', '09-08', '09-09', '09-10', '09-11', '09-12', '09-14', '10-08']
16
['04-04', '04-11', '07-04', '07-11', '10-15', '11-05']
5366 4015 4075
```

Twelve alarms with the median: the two campaigns, the outage and the level
shift in September. The six extra alarms with the mean all fall in the weeks
**after** an anomaly, on the same weekday: perfectly ordinary days compared
with a spoilt expectation. On 21 March the mean expects 5366 because it takes
in the campaign of a week earlier.
