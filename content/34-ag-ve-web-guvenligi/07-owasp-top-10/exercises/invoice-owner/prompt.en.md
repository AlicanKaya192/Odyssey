`invoices` is a list of invoices, each `{"id", "owner", "amount"}`.
`get_invoice(invoices, user, invoice_id)` should return the amount
(`amount`) if the invoice exists **and** its owner is `user`. If the
invoice does not exist or belongs to someone else, it should give the same
answer for both: `"not found"`. The starter code ignores ownership.

**Expected output:**

```
250
not found
not found
```
