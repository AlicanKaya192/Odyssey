The `config` dictionary has the keys `debug`, `admin_password`,
`dir_listing` and `https_only`. `audit(config)` should return the codes of
the problems found as a list **in this order**: `"debug"` (debugging on),
`"default-password"` (the password is `admin`, `password` or `1234`),
`"listing"` (directory listing on), `"http"` (`https_only` off).

**Expected output:**

```
['debug', 'default-password', 'http']
[]
```
