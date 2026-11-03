`audit_handshake(info)` should check a handshake summary (`version`,
`suite`, `cert_ok`, `finished_ok`) and return a list of problems, in this
order: `"old version"` if the version is not `TLSv1.3` or `TLSv1.2`,
`"weak suite"` if the suite is not in `STRONG_SUITES`, then `"bad
certificate"`, `"bad finished"`. The starter code looks only at the last
two. With no problems, an empty list.

**Expected output:**

```
[]
old version
weak suite
```
