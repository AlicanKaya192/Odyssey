`stopped_at(log)` should read the step log: a list of `[step, succeeded,
tokens]` triples. Return the name of the first failed step and the total
tokens of all steps as `[step, total]`; if no step failed, `"done"`
instead of the step.

**Expected output:**

```
['extract', 83]
['done', 170]
```
