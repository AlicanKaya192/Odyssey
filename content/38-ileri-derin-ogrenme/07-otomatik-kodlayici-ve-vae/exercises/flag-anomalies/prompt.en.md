`flag_anomalies(errors, train_errors, q)` should take the threshold as the
`q` quantile of the training errors (`torch.quantile`) and return, for every
error, whether it **exceeds** the threshold, as a boolean list.

**Expected output:**

```
[False, True, True]
[False, True, True]
```
