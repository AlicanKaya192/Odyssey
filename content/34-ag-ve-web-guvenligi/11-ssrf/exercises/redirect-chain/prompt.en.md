`chain` holds the addresses a request followed (the first request and
the redirects). `first_bad(chain, hosts)` should check every step: the
scheme must be `http`/`https` and the host in `hosts`. Return the index
(from 0) of the **first** address that fails the check; `-1` if all
pass. The starter code looks only at the first address.

**Expected output:**

```
2
-1
```
