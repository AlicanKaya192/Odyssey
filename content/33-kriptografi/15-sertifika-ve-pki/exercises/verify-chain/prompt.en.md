`digest`, `tbs` and `check_signature` are ready. `verify_chain(chain,
trusted)` checks every link from the site to the root, but never looks at
whether the root at the top of the chain is in the **trust store**. Add it:
`trusted` is a dictionary mapping a name to `[e, n]`; if the top
certificate's name and key are not there, return `"untrusted root"`.

**Expected output:**

```
ok
untrusted root
```
