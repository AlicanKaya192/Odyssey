Produce a summary of the first 50 000 payments without keeping the events in
a list.

**What to do:**

1. In the loop `for event in payments(50_000):` update: the number of
   payments, the total amount, the number of payments over 1000, and the
   largest payment (the event itself).
2. After the loop print, in order: the number of payments, the total (two
   decimals), the mean (two decimals), the number of payments over 1000.
3. On the last line print the `event_id` and amount of the largest payment.

You do not need a list (`list(...)`, `append`).

**Expected output:**

```
50000
6185404.53
123.71
60
24849 3423.02
```
