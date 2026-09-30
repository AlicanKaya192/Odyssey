Catch the level shift with CUSUM and see the effect of clipping, of the
allowance and of the threshold.

In the starter code `z` is ready: the relative deviation standardised against
the January–February reference (not clipped).

**What to do:**

1. Write the function `cusum(z, k, h)`. The sum starts from zero; every day
   `total = max(0, total + value - k)`. If the sum passes `h` that day is
   added to the list of alarms and the sum is **reset to zero**. It returns
   the list of alarm days.
2. With the clipped series (`z.clip(-3, 3)`), `k = 1`, `h = 8`: print the day
   of the first alarm (`"%Y-%m-%d"`), how many days after 2 September that is
   and the total number of alarms, on one line.
3. Print the day of the first alarm with the unclipped `z` and the same
   settings.
4. With the clipped series and `k = 0.5`, `h = 5`: print the alarm days
   **before** 2 September as a `"%m-%d"` list.

**Expected output:**

```
2024-09-05 3 23
2024-03-14
['03-11', '05-10', '06-13']
```

The clipped CUSUM stays quiet for eight months and catches the shift three
days later. But because the reference is not updated it goes on ringing until
the end of the year: an alarm means "renew the reference". Without clipping
the single campaign day on 14 March crosses the threshold on its own. The more
sensitive setting (`k = 0.5`, `h = 5`) gives three false alarms before
September.
