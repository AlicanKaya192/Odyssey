Log lines look like `"10:01 sudo user=bob result=denied cmd=passwd"`:
a time, `sudo`, then `key=value` fields. `denied_users(lines, threshold)`
should return, in alphabetical order, the users whose number of
`result=denied` lines is **equal to or greater than** `threshold`.

**Expected output:**

```
['bob']
['bob', 'eve']
```
