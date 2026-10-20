The gate in the pipeline is a separate script. The training script
writes the measurements to `metrics.json`, and the gate script reads them
and decides. A sketch:

```python
import json
import sys

RULES = {"min_accuracy": 0.78, "min_lift": 0.05, "min_slice": 0.75}

metrics = json.loads(open("metrics.json", encoding="utf-8").read())
failures = []
if metrics["accuracy"] < RULES["min_accuracy"]:
    failures.append("accuracy below the floor")
if metrics["accuracy"] < metrics["baseline"] + RULES["min_lift"]:
    failures.append("too close to the baseline")
for name, value in metrics["slices"].items():
    if value < RULES["min_slice"]:
        failures.append(f"{name} slice too low")

for failure in failures:
    print("FAIL:", failure)
sys.exit(1 if failures else 0)
```

- Training and the gate are **separate** scripts: when the gate's rules
  change, there is no need to retrain the model; the measurements are in
  the file.
- `sys.exit(1)` makes the step turn red; GitHub Actions tells whether a
  step succeeded by its exit code.
- Every problem is written on its own line: the pipeline's log shows why
  it failed.

## Checklist

- Does the gate run on every pull request?
- Are the data and the seed of the training in CI fixed? (If not, the
  gate passes sometimes and fails sometimes: a flaky test.)
- Is there a separate bar for every slice?
- Are the measurements kept with `if: always()`?
- Are the thresholds written down somewhere, with reasons?

## Don't

- Don't lower the threshold to get past a failing gate; first look at
  why it failed.
- Don't tie the gate only to the average; slices get lost in the
  average.
- Don't run hours of training in CI; the pipeline slows down and nobody
  waits.
