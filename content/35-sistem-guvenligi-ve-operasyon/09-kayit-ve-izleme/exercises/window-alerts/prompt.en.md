`times` are failure seconds sorted from smallest to largest.
`window_alerts(times, window, limit)` should, after each new event, count
the events in the last `window` seconds (those **greater** than
`t - window`) and, if the count has reached `limit`, add that event's
second to the list. Return the list.

**Expected output:**

```
[31, 44, 220]
[]
```
