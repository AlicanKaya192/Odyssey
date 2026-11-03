Each rule in `rules` is `[key, wanted, advice]`.
`hardening_findings(config, rules)` should return the advice of every rule
whose value in the configuration does not equal the wanted value, in rule
order. A key that is **absent** from the configuration also counts as
failing (the starter code raises `KeyError` there).

**Expected output:**

```
turn on the firewall
disable guest
encrypt the disk
```
