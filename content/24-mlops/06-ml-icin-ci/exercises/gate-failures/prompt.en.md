Write the function `gate_failures(metrics, rules)` and return the list of rules that failed:

- If the accuracy is less than `rules["min_accuracy"]`, `"accuracy"`.
- If the accuracy is less than `metrics["baseline"] + rules["min_lift"]`, `"lift"`.
- For every slice in `metrics["slices"]`, **in alphabetical order of their names**: if its value is less than `rules["min_slice"]`, `"slice:<name>"`.

If no rule failed, an empty list.

**Expected output:**

```
[]
accuracy
lift
slice:basic
slice:pro
```
