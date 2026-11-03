`chain(entries)` in the starter code builds the hash chain (do not change
it). `first_tampered(entries, saved)` should recompute the chain of the
lines, compare it with the saved hashes (`saved`) and return the index
(from 0) of the **first** line that does not match. If all match, return
`-1`.

**Expected output:**

```
-1
1
0
```
