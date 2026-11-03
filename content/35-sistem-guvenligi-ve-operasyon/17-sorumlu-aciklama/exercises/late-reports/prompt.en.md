Each report is `[id, received, acknowledged]`; if not yet acknowledged,
the last field is `None`. `late_reports(reports, today, limit)` should
return, sorted, the ids of reports whose acknowledgement took longer than
`limit` days. For an unanswered report, the time is counted up to today.

**Expected output:**

```
['R-2', 'R-4']
```
