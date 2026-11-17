`warmup_rates(base, warm, epochs)` should build a warmup that raises the rate
linearly over the first `warm` epochs: in epoch `e` the factor is
`min(1, (e + 1) / warm)`. `lr_scheduler.LambdaLR(optimizer, function)` takes a
function that gives the factor. The starter code already collects the rates;
add the scheduler.

**Expected output:**

```
[0.025, 0.05, 0.075, 0.1, 0.1, 0.1]
```
