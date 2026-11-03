Each record is `[id, purpose, created]` (the date is ISO text);
`retention` is purpose → days. `to_delete(records, retention, today)`
should return, in alphabetical order, the ids of the records to delete:
those whose age **exceeds** their purpose's period, and those whose purpose
is **not** in `retention` (there is no basis to keep them).

**Expected output:**

```
['r1', 'r5']
```
