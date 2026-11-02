A payment dictionary: `amount`, `created_by`, `approvals` (the list of
approvers). `approve(payment, approver)` should handle one approval and
return the status:

1. If the approver is the person who prepared the payment → `"denied"`.
2. If the approver is already in the list → `"duplicate"`.
3. Otherwise **add** the approver to the `approvals` list.
4. Approvals needed: **2** if the amount is `10000` or more, otherwise
   **1**. If there are enough approvals → `"approved"`, otherwise →
   `"pending"`.

**Expected output:**

```
ada denied
alan pending
alan duplicate
grace approved
small approved
```
