`after_decay(start, lr, decay, steps)` should take `steps` steps with
`SGD(lr, weight_decay=decay)` on a loss whose gradient is always 0 (`w · 0`) and
return the final weight with 4 places. The result should be
`start · (1 − lr · decay)^steps`.

**Expected output:**

```
0.9703
1.62
```
