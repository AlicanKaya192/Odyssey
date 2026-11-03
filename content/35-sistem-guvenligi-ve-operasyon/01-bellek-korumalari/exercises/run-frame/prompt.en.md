`run_frame(size, canary, data)` should build a frame: `size` zeros, then
the canary, then a return slot (`0`). It should write `data` from the
start but **not** past the end of the frame (the toy memory does not
grow). Then it should look at the canary: return `"ok"` if it is intact,
`"detected"` if it has changed.

**Expected output:**

```
ok
ok
detected
detected
```
