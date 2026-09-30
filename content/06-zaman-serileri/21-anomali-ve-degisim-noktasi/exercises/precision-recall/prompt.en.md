Test the threshold of the detector against the 12 events of the maintenance
log: precision and recall.

In the starter code `score` (the robust score from the hour profile) and
`events` are ready.

**What to do:**

1. Write the function `evaluate(threshold, skip)`:
   - leave the hours in `skip` out of the score (`score.drop(skip)`)
   - find the hours whose absolute score passes the threshold
   - return four values as a tuple: the number of alarms, how many of them are
     in `events`, the precision (correct / alarms) and the recall (correct /
     number of events); the ratios with two decimals.
2. Print the result for a threshold of 3 with nothing skipped (`skip=[]`).
3. Set the stuck-sensor hours aside:
   `stuck = pd.date_range("2024-09-30 08:00", "2024-09-30 16:00", freq="h")`.
   For thresholds 2, 2.5, 3, 4 and 6 print the result with `skip=stuck`
   together with the threshold, one per line.
4. Print the events missed at a threshold of 4 as a `"%m-%d %H"` list.

**Expected output:**

```
(20, 12, 0.6, 1.0)
2 (38, 12, 0.32, 1.0)
2.5 (16, 12, 0.75, 1.0)
3 (12, 12, 1.0, 1.0)
4 (10, 10, 1.0, 0.83)
6 (8, 8, 1.0, 0.67)
['09-28 19', '10-04 12']
```

On the first line the precision looks like 0.6: 8 of the 20 alarms are not in
the log. But those eight are the stuck sensor: a real problem, just not
written in the log. With them set aside a threshold of 3 is perfect. As the
threshold falls false alarms multiply (26 at a threshold of 2); as it rises
small events are missed. Before saying "false alarm" look at what the alarm
coincides with: the labels can be incomplete too.
