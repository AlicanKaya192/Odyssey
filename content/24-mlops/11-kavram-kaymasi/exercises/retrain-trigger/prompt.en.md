Write the function `should_retrain(alert, months_since, every)` for the schedule + emergency trigger rule:

- `alert`: whether the quality alert went off (`True` / `False`).
- `months_since`: months since the last training.
- `every`: the schedule's interval (months).
- Return `"retrain"` if the alert went off or `months_since` is at least `every`, otherwise `"wait"`.

**Expected output:**

```
wait
retrain
retrain
```
