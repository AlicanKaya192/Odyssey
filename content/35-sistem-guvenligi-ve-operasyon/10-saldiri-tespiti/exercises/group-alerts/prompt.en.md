Each alert is `[second, source]`. `group_alerts(alerts, gap)` should
group the alerts by source: in a source's alerts sorted by time, two alerts
whose gap is **not longer** than `gap` seconds belong to the same event.
For each event return a `"<source> <first>-<last> (<count>)"` line, sorted
by source, then by first second.

**Expected output:**

```
198.51.100.4 30-30 (1)
203.0.113.9 10-15 (3)
203.0.113.9 90-90 (1)
```
