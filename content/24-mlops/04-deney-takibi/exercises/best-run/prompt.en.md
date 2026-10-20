The experiments in the log are a list: every experiment has `"run"` (the number) and the dictionaries `"params"` and `"metrics"`. Write the function `best_run(runs, metric)`:

- Return the **number** of the experiment whose `metric` measurement in `metrics` is the highest.
- Skip the experiments that don't have that measurement.
- On a tie, the earlier one (earlier in the list) wins.
- If no experiment has that measurement, return `None`.

**Expected output:**

```
2
3
None
```
