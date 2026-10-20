Write the function `decide(score, threshold, customer)` that falls back to the rule when the model goes down:

- If `score` is `None`, the model didn't run: make an offer if the customer's `"support_calls"` is at least `2`.
- Otherwise make an offer if `score` is at least `threshold`.
- Return `"offer"` for an offer, otherwise `"no offer"`.

**Expected output:**

```
offer
no offer
offer
no offer
```
