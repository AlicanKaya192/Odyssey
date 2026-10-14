In a team's pipeline three things may or may not happen automatically: testing, packaging and releasing.

Write the function `release_kind(tests_auto, package_auto, release_auto)`. All three values are `True` or `False`:

- If the tests are not automatic: `"manual"`
- If the tests are automatic but packaging is not: `"continuous integration"`
- If packaging is automatic too but releasing is not: `"continuous delivery"`
- If all three are automatic: `"continuous deployment"`

**Expected output:**

```
manual
continuous integration
continuous delivery
continuous deployment
```
