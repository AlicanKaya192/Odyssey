`find_secrets(source)` should return the line numbers (starting at 1) of
built-in secrets in the source code. A line is a secret if it assigns a
**quoted** value to a variable whose name contains `key`, `secret`,
`password` or `token`; upper or lower case does not matter. The starter
code's regular expression only looks for `password`.

**Expected output:**

```
[2, 5]
```
