`controls` is a list where each item is `[name, function]`. `FUNCTIONS`
holds the six NIST CSF functions in order.

`csf_summary(controls)` should return a list of `[function, count]` pairs
for all six functions in `FUNCTIONS` order; a function with no controls is
in the list with `0` too. A function not in `FUNCTIONS` is not counted.

**Expected output:**

```
Govern 0
Identify 1
Protect 2
Detect 1
Respond 0
Recover 1
```
