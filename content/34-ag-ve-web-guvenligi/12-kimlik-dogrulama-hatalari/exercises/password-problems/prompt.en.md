`password_problems(password, user, common)` should return the list of
problems **in this order**: `"too short"` if it is shorter than 8
characters; `"common"` if its lower-case form is in `common`;
`"contains user name"` if it contains the user name (case-insensitive).

**Expected output:**

```
qwerty ['too short', 'common']
Ada2026! ['contains user name']
blue-river-under-stone []
PASSWORD ['common']
```
