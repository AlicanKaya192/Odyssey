Fit four ARIMA candidates to the share price and see whether going beyond
a plain random walk gains anything.

`k` (the price, as a numpy array) is ready in the starter code.

**What to do:**

1. Four candidates: `(0, 1, 0)`, `(1, 1, 0)`, `(0, 1, 1)`, `(1, 1, 1)`. For
   each print the AIC with one decimal as `order AIC`, one per line.
2. Print the difference between the smallest and the largest AIC with one
   decimal.
3. Print the AR and MA coefficients (`ar.L1`, `ma.L1`) of the `(1, 1, 1)`
   model with two decimals on one line.
4. Print the 3-step forecast of the `(0, 1, 0)` model and the last value of
   the series with two decimals on one line (the forecast list first).

**Expected output:**

```
(0, 1, 0) 3503.1
(1, 1, 0) 3503.8
(0, 1, 1) 3503.9
(1, 1, 1) 3503.1
0.8
0.63 -0.57
[166.44, 166.44, 166.44] 166.44
```

The AICs of the four models are within one point: the extra terms gain
nothing. The two coefficients of `(1, 1, 1)` are close in size and opposite in
sign: they cancel each other. The forecast of the plainest model is the last
value itself: the best forecast for a random walk is naive, and ARIMA confirms
it.
