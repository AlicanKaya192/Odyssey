`canonical_email(email)` should remove leading and trailing spaces and
turn it to lower case. If the result does not have **exactly one** `@`,
or the left or right of `@` is empty, return `None`; if it is valid,
return the canonical form.

**Expected output:**

```
'ada@example.com'
None
None
None
```
