Write simple exponential smoothing yourself with a loop and compare it
with the result of pandas. `y` is ready in the starter code: the sales of
1–14 September 2024.

**What to do:**

1. Write the function `smooth(values, alpha)`: start the level at the first
   value; for each value apply
   `level = alpha * value + (1 - alpha) * level` and return the levels as a
   list.
2. With `α = 0.5` print the first 5 levels, rounded to one decimal, as a list.
3. Compute the same with pandas (`y.ewm(alpha=0.5, adjust=False).mean()`) and
   print the first 5 values.
4. Are the two results the same on all 14 days? Print whether the largest
   absolute difference is below `1e-9`.
5. The forecast for 15 September is the last level. Print that forecast for
   `α = 0.1`, `0.5` and `0.9`, rounded to one decimal, as a list.
6. Print the actual value of 15 September.

**Expected output:**

```
[351.0, 287.0, 255.0, 259.5, 261.8]
[351.0, 287.0, 255.0, 259.5, 261.8]
True
[312.4, 337.4, 373.9]
353
```

The same 14 days, three different forecasts. Because the last day (a Saturday)
is high, a large `α` pulls the forecast up; a small `α` stays close to the
average of the two weeks. The middle forecast happened to land near Sunday's
value (353), but the model says the same number for the whole horizon: 337 for
Monday too. Yet the Mondays of these two weeks were 223 and 270. Simple
exponential smoothing does not know the weekly pattern; it is not used on its
own for a seasonal series.
