Each storage area is a dict with `name`, `public`, `encrypted`, `data`.
`bucket_findings(buckets)` should return finding lines in alphabetical
order by name; within one area, access first, then encryption:

- `"<name>: public with <data> data"` if public but `data` is not `"public"`,
- `"<name>: not encrypted"` if unencrypted.

**Expected output:**

```
exports: public with personal data
exports: not encrypted
logs: not encrypted
```
