Measure the effect of a campaign and of a holiday by comparing each event
day with **the same weekday** a week before and a week after.

**What to do:**

1. Write a function `effect(flag)`. `flag` is `"promo"` or `"holiday"`. For
   every day on which that column is 1:
   - Take the days 7 days before and 7 days after.
   - Keep those that **are** in the index and are neither a campaign day nor
     a holiday.
   - If at least one neighbour is left, append the day's sales minus the mean
     of the neighbours to a list.
   The function returns the mean of the list (one decimal) and the number of
   elements as a tuple.
2. Print the results of `effect("promo")` and `effect("holiday")`, one per
   line.
3. For comparison print the rough effects: for each flag, the mean of the days
   where it is 1 minus the mean of the days where it is 0 (one decimal, on one
   line; the campaign first).

**Expected output:**

```
(50.8, 84)
(-76.2, 41)
57.0 -67.3
```

In the fair comparison a campaign is +51 and a holiday −76. The rough
calculation overstated the campaign and understated the holiday: campaigns
fall on the busy days of the working week, and holidays in the warm months
when sales are high anyway. The true values (the data was generated this way)
are +48 and −75.
