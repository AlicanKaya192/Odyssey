R² is a one-line call, but the previous section's baseline is hidden inside
it. Spelling the formula out makes that visible.

```
R² = 1 - (the model's error) / (the baseline's error)
```

**What you need to do:**

1. Read `homes.csv`, take `area` and `price`, split it the usual way (a
   quarter for testing, `random_state=42`) and train the model.
2. Compute **`ss_res`**: the **sum** of the squared residuals (not their
   mean). Print it to two decimals.
3. Compute **`ss_tot`**: each actual value's distance from the **test
   mean**, squared and summed. Print it to two decimals.
4. Compute R² as `1 - ss_res / ss_tot`.
5. Print your own result and the one `r2_score` gives **side by side**
   (three decimals).

**Expected output:**

```
5225.02
91593.28
0.943 0.943
```

**What the two numbers mean:**

- `ss_res` **5225** — the model's total squared error.
- `ss_tot` **91593** — the total squared error of a baseline that predicts
  the mean for everything.

The model left only **5.7%** of the baseline's error. R² 0.943 says exactly
that: `1 - 5225/91593`.

**Three readings follow from this:**

- R² **1** means `ss_res` is zero: no error at all.
- R² **0** means `ss_res` equals `ss_tot`: the model is as good as the
  baseline.
- R² **negative** means `ss_res` is larger: the model predicts worse than
  the mean.

**One detail:** the baseline here is the **test** set's mean; in the
previous section you used the **training** mean. The two come out close but
are not the same, and this is the one R²'s zero point is built on.
