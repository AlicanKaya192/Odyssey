Each finding is `[id, severity]`; the severity is `critical`, `high`,
`medium` or `low`. `fix_order(findings)` should return the ids in fix
order: first by severity (critical first), within the same severity in
alphabetical order by id. An unknown severity comes last.

**Expected output:**

```
F-2
F-3
F-1
F-5
F-7
F-9
```
