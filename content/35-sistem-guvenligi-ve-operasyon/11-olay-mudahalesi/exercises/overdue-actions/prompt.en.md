Each action item is `[id, owner, due_date, done]`. `overdue_actions(actions,
today)` should return the items that are not done and whose due date is
**before** `today`, as `"<id> <owner> <due_date>"` lines; sorted by due
date, then by id. Compare the dates with `date.fromisoformat`.

**Expected output:**

```
A-5 ada 2026-10-01
A-1 bob 2026-10-20
A-4 bob 2026-10-20
```
