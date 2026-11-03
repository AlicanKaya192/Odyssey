Each line is a JSON log object carrying a `level` field.
`count_levels(lines)` should return the number of lines per level as
`"<LEVEL>: <count>"` lines, in alphabetical order by level name. A line
that cannot be read as JSON must **not stop** the program; it is counted
under the `INVALID` level (a broken line is a signal too).

**Expected output:**

```
ERROR: 1
INFO: 1
INVALID: 1
WARNING: 2
```
