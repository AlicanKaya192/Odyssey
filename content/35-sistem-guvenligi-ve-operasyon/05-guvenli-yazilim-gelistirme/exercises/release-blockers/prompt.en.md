`release_blockers(checklist, required)` should look at the checklist for
every item in `required`: an item blocks the release if it is **absent**
from the checklist or its value is `False`. Return the blocking items in
alphabetical order. The starter code raises `KeyError` for a missing
item.

**Expected output:**

```
dependencies_scanned
security_tests_pass
```
