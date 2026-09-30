Seasonal naive, or the mean of the last four weeks? Compare the two on the
same 13 experiments and decide whether the difference is real.

In the starter code `snaive(train, h)`, `weeks_mean(train, h, k)` and `cuts`
(the 13 cut days) are ready.

**What to do:**

1. Write a function `errors(forecast)`: in each of the 13 experiments it
   computes the 28 days of **absolute errors** and returns them all as a
   13 × 28 numpy array. `forecast` is a function taking `(train, h)`.
2. Run it for two methods: `snaive` and
   `lambda train, h: weeks_mean(train, h, 4)`.
3. Take the MAE per experiment of each method (the mean along `axis=1`) and
   print the overall mean of the two methods, with two decimals, on one line
   (seasonal naive first).
4. Compute the difference experiment by experiment (`snaive − weeks`). Print
   its mean, its standard deviation (`ddof=1`, two decimals) and the number of
   experiments seasonal naive wins, on one line.
5. What would someone looking only at experiment 12 (the 5 November cut,
   position 11 in the array) have seen? Print the MAE of the two methods in
   that experiment, with two decimals, on one line.
6. Average the error of each method by the week of the horizon (split the
   columns into four pieces of 7) and print two lists with one decimal, one
   per line.

**Expected output:**

```
17.95 17.2
0.75 2.84 5
11.64 14.84
[15.9, 17.0, 18.2, 20.7]
[13.9, 16.4, 17.9, 20.6]
```

On average the four-week method is a little ahead, but the gap (0.75) is far
below its variation between experiments (2.8), and seasonal naive wins 5 of
the 13 experiments. Someone looking at a single experiment would have reached
the opposite conclusion. The honest decision: a tie. The last two lines give a
small detail: the four-week mean is a little better at the near horizon and
the gap closes further out.
