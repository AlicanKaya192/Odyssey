`verify_chain`, `date_status` and `host_matches` are ready.
`check_site(chain, trusted, host, today)` should check, in order, the
chain, the date of the site certificate (`chain[0]`) and its name
(`subject`); it should return the result of the first failing step
(`verify_chain`'s message, `date_status`'s message or `"name mismatch"`),
and `"ok"` if all pass. The starter code only looks at the chain.

**Expected output:**

```
ok
expired
name mismatch
```
