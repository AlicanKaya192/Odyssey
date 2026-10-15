Write the function `rollback_target(history)`. `history` is the list of deployments, oldest to newest; each item is `[version, status]` and the status is `"ok"` or `"failed"`. **The last item is the deployment running now.**

The version to roll back to: among the deployments before it, the newest version whose status is `"ok"` and that is **different from the current version**. `None` if there is none.

`reversed(...)` can be used to go through the list from the end.

**Expected output:**

```
1.2.1
None
None
1.0.0
```
