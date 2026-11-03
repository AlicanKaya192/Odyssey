`csp_problems(header)` should check a CSP value and return the problem
codes as a list **in this order**. Script sources are read from
`script-src`, or from `default-src` if that is missing. If both are
missing, just `["no-script-src"]`. If the sources contain
`'unsafe-inline'`, `"unsafe-inline"`; if they contain `*`, `"wildcard"`.
Directives are separated by `;` and the first word is the directive's
name.

**Expected output:**

```
[]
['unsafe-inline']
['no-script-src']
['wildcard']
```
