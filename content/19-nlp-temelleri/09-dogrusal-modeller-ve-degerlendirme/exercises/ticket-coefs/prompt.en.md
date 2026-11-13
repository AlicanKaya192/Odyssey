`top_words(label, k)` should return the `k` words with the **largest
coefficients** for that class in the ticket classifier, largest first. The
model and `words` are ready; the class's row is in `model.coef_`, in
`model.classes_` order.

Words with equal scores should come in alphabetical order:
`np.argsort(-score, kind="stable")` sorts from largest to smallest and
keeps equal ones in place, so the order is the same on every computer.

**Expected output:**

```
account account, email, com
billing charged, invoice, billing
refund refund, will, back
shipping delivered, it, arrived
technical app, error, page
```
