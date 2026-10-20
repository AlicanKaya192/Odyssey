Write the function `rollout(stages, decisions)` that processes a canary's daily decisions:

- `stages`: the shares, for example `[1, 5, 25, 100]`. The release starts at the first share.
- For each decision: `"advance"` moves to the next share (stays there if it is already at the last one), `"wait"` stays at the same share, `"rollback"` sets the share to `0` and ends the release (later decisions aren't processed).
- Add the share after every decision to a list and return the list.

**Expected output:**

```
[1, 5, 25, 100, 100]
[5, 0]
[]
```
