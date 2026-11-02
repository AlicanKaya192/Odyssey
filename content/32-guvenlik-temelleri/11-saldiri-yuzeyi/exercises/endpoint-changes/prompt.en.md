`endpoint_changes(old, new)` should compare two releases' endpoint
lists and return this dictionary:

- `"added"`: those only in `new`,
- `"removed"`: those only in `old`.

Both lists should be in alphabetical order and without repeats.

**Expected output:**

```
added ['/debug', '/export']
removed ['/old']
```
