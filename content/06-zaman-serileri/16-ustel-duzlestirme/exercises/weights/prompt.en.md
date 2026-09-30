In exponential smoothing the weight of the observation `k` steps back is
`α × (1 − α) ** k`. See in numbers how these weights behave.

**What to do:**

1. Write the function `weights(alpha, n)`: it returns the weights of the
   newest `n` observations (k = 0, 1, ..., n − 1) as a list.
2. For `α = 0.3` print the first 6 weights, rounded to three decimals, as a
   list.
3. For `α = 0.3` print the sum of the first 10 weights, rounded to three
   decimals.
4. For `α = 0.9` print the first 3 weights with three decimals as a list.
5. How many of the newest observations are needed for the weights to add up to
   more than 0.95? Find that number for `α = 0.1`, `0.3` and `0.9` and print
   them as a list.

**Expected output:**

```
[0.3, 0.21, 0.147, 0.103, 0.072, 0.05]
0.972
[0.9, 0.09, 0.009]
[29, 9, 2]
```

With `α = 0.9`, 90% of the weight is on a single observation: almost the naive
forecast. With `α = 0.1` it takes 29 observations to reach 95% of the weight:
the forecast behaves like the average of about a month of the past. A single
number decides how far back the model looks.
