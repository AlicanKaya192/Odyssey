Pull the Least Privilege section together. `grants` is user → granted
permissions, `used` is user → those used in the last 90 days (none if the
user is missing), `conflicts` are `[a, b]` pairs that must not be held
together.

`access_report(grants, used, conflicts)` should return the lines as a list.
Users in alphabetical order; for each user first every unused permission
(alphabetical) as `"<user>: unused <permission>"`, then every conflict
whose two permissions they hold (in the given order) as
`"<user>: conflict <a>+<b>"`.

**Expected output:**

```
ada: unused read-reports
ada: conflict pay-create+pay-approve
bora: unused read-reports
ceren: unused read-logs
```
