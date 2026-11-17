`predict_all(weight, rows)` should predict every row's class: the logits are
`rows · Wᵀ`, the prediction is the position of the largest logit. Remove the
row-by-row loop at the start; compute all rows with **one product**, inside
`torch.inference_mode()`, and return the list.

**Expected output:**

```
[0, 1, 2]
```
