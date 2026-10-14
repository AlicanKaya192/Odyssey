`output_problems(reply, canary, allowed)` should return the list of
problems in the answer: `"leaks the system message"` if `canary` appears
in the answer; `"link to <domain>"` for every domain found by the given
`LINK` pattern that is not in `allowed` (in the answer's order).

**Expected output:**

```
ok
['leaks the system message']
['link to bad.example']
```
