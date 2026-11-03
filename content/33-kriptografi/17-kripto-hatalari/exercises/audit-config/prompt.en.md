`audit(config)` should list the problems in an encryption configuration
in this order: `"ecb mode"` if `mode` is `"ECB"`, `"fixed nonce"` if
`nonce` is `"fixed"`, `"no integrity"` if `mac` is `False`, `"low
iterations"` if `kdf_iterations` is below 600000, `"tls verification off"`
if `verify_tls` is `False`. The starter code only does the first and last
checks.

**Expected output:**

```
[]
fixed nonce
no integrity
low iterations
```
