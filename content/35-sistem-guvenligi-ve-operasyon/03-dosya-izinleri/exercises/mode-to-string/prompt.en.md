`mode_to_string(mode)` should turn a permission number (such as `0o750`)
into the nine-letter string: `"rwxr-x---"`. Owner, group and others in
order; in each class look at the `r` (4), `w` (2), `x` (1) bit, write `-`
if it is off. Do not use `stat.filemode`: the point is to read the bits
yourself.

**Expected output:**

```
0o755 rwxr-xr-x
0o640 rw-r-----
0o600 rw-------
0o7 ------rwx
```
