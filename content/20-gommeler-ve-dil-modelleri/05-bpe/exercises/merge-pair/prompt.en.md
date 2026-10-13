`merge_pair(symbols, pair)` should join the two symbols into one wherever
`pair` (a two-item list) occurs next to each other. Go left to right; merged
symbols are not used again (`a a a` + `a a` → `aa a`).

**Expected output:**

```
['lo', 'w', '</w>']
['aa', 'a']
```
