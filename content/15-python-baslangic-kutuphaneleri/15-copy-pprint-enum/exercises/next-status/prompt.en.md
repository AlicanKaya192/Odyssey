The ready `Status` enum holds the order statuses in order: `pending`,
`paid`, `shipped`, `delivered`. Write the function `next_status(value)`:
return the value of the **next** status after the given one; `None` if it is
the last status, `"invalid"` if the value is invalid. `list(Status)` gives
the order.

**Expected output:**

```
paid
delivered
None
invalid
```
