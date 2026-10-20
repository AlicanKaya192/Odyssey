To see the effect of a setting, take the **mean** of the measurement for each value of that setting. Write the function `mean_by_param(runs, param, metric)`:

- Skip the experiments whose `params` don't have `param`.
- For each value of the setting, round the mean of the `metric` measurements to three digits.
- Return a list `[[value, mean], ...]`; the values in the order they **first appear** in the experiments.

**Expected output:**

```
max_depth 3 0.785
max_depth 5 0.815
```
