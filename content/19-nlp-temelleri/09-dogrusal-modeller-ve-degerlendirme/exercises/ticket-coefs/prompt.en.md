`top_words(label, k)` should return the `k` words with the **largest
coefficients** for that class in the ticket classifier, largest first. The
model and `words` are ready; the class's row is in `model.coef_`, in
`model.classes_` order.

**Expected output:**

```
account account, email, example
billing charged, invoice, billing
refund refund, will, back
shipping delivered, it, arrived
technical app, error, page
```
