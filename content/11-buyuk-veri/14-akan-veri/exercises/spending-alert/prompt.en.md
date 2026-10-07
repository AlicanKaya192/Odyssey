Alert when a card spends more than 1000 in total in the last 120 seconds.

**What to do:**

1. For each card keep its recent payments as `(ts, amount)` in a `deque`,
   and the window's total in a separate dictionary.
2. At every payment: add the payment, add to the total; remove from the left
   the ones whose `ts` is `event["ts"] - 120` or older, and subtract them
   from the total.
3. Alert **once, the moment the limit is passed**: the total before the
   payment was 1000 or less, now it is more than 1000.
4. For `payments(20_000)` print the first three alerts as
   `event_id card total` (total with two decimals), then print the number of
   alerts.

**Expected output:**

```
708 C086 1016.64
869 C053 1057.89
1331 C183 1002.36
70
```
