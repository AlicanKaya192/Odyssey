`mask_email(address)` should keep only the first letter of the user part
and return the form `"a***@example.org"`. If the text has no `@`, return
`"***"`.

**Expected output:**

```
a***@example.org
b***@mail.example.org
***
```
