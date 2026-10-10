Customers were insured for different numbers of days (`days`). `claim_model()` should
train the Poisson GLM with `offset=np.log(d3["days"])` and return
`[risk_rate_ratio, constant]` (the rate ratio via `np.exp`; both with 3
places). The starter code forgets the offset.

**Expected output:**

```
[1.578, -3.958]
```
