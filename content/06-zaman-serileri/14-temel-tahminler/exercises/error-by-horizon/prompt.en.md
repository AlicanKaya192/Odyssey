Measure on two series how the error grows as the forecast horizon
lengthens.

**What to do:**

1. For the share price the error of the naive forecast `h` steps ahead is
   `(k.shift(-h) - k).abs().mean()`. Compute it for `h = 1, 5, 10, 20, 40`
   and print the values, rounded to two decimals, as a list.
2. Print the ratio of the 40-day error to the 1-day error and the value of
   `40 ** 0.5`, rounded to one decimal, on one line.
3. For the daily sales the error of seasonal naive `w` weeks ahead is
   `(s - s.shift(7 * w)).abs().mean()`. Compute it for `w = 1, 2, 4, 8` and
   print the values, rounded to one decimal, as a list.
4. For the daily sales print the error of **plain** naive 1, 3 and 7 days
   ahead (`(s - s.shift(h)).abs().mean()`), rounded to one decimal, as a list.

**Expected output:**

```
[1.83, 4.5, 6.42, 8.76, 12.16]
6.7 6.3
[13.4, 14.4, 17.5, 22.9]
[36.8, 70.3, 13.4]
```

For the share price the error grows with the horizon, but at a horizon 40
times as far it is only 6–7 times as large: square-root growth. For the sales
the error of seasonal naive creeps up from week to week. The last line is
surprising: with plain naive the error 7 days ahead is far **smaller** than
3 days ahead. Seven days ahead is the same weekday again; in a seasonal series
what is "near" is not the neighbouring day in the calendar but the same
position in the pattern.
