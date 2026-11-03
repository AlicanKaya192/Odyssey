`scope_check(target, day, scope, excluded, window)` takes the target
address (text), the day (ISO text), the scope networks (a list of CIDRs),
the excluded addresses and the window (`[start, end]`, both days
included). It should check in order and return `"outside the window"`,
`"excluded"`, `"out of scope"` or `"in scope"`. The starter code is
missing one check.

**Expected output:**

```
in scope
excluded
out of scope
```
