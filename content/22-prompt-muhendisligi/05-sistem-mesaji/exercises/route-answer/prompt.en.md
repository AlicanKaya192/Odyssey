`route(problems)` should say the path from the list of problems the
check found: `"human"` if the list contains `"promise"`; `"retry"` if
there is another problem; `"send"` if the list is empty.

**Expected output:**

```
[] send
['too long'] retry
['too long', 'promise'] human
```
