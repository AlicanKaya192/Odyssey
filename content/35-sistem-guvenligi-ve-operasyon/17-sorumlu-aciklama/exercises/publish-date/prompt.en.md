`publish_date(reported, fixed, deadline_days, grace_days)` should return
the announcement day as ISO text: the deadline is the report day +
`deadline_days`. If there is a fix day (`fixed`), whichever is earlier of
fix + `grace_days` and the deadline; if there is no fix (`None`), the
deadline.

**Expected output:**

```
2027-01-24
2027-02-01
2027-02-01
```
