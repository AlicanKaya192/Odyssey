There are two models, and the actual value is 100 every time.

- **Model A** is off by 10 units on every prediction.
- **Model B** gets nine exactly right and misses one by 100 units.

Which is better? Measure first.

**What you need to do:**

1. Import the two functions you need from `sklearn.metrics`.
2. Compute **MAE** and **RMSE** for both models. (sklearn does not give RMSE
   directly; you take the square root of MSE yourself.)
3. Print one line per model: **the model's name, MAE, RMSE** — the three
   side by side, numbers to two decimals.

**Expected output:**

```
a 10.0 10.0
b 10.0 31.62
```

**MAE cannot tell them apart.** Both are 10.0. As far as MAE is concerned
these two models are identical.

**RMSE can.** B's single large error, once squared, brings three times the
penalty.

**Which one is right?** Not the measure but the problem decides:

- For a delivery-time estimate a ten-minute deviation is tolerable, but
  being 100 minutes out on one order loses the customer. **B is the bad
  model, RMSE is right.**
- For a monthly total cost estimate small deviations accumulate while one
  large deviation dissolves into the average. **A is the bad model, MAE is
  right.**

Choosing a measure is not a technical decision but a **business** one.
Whatever the answer to "is one large error more expensive than the sum of
several small ones", that is your measure.
