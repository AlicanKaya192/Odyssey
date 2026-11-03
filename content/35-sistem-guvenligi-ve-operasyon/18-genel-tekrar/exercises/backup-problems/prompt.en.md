Each copy is `[media, offsite, hours_ago]`. `backup_problems(copies,
rpo_hours)` should return the problems in this order: `"fewer than 3
copies"`, `"fewer than 2 media"` (the number of different media), `"no
offsite copy"`, `"newest copy too old"` (the newest copy is older than
`rpo_hours`, or there is no copy). Backup and Disaster Recovery.

**Expected output:**

```
GOOD
SAME
- fewer than 2 media
BAD
- fewer than 3 copies
- fewer than 2 media
- no offsite copy
- newest copy too old
```
