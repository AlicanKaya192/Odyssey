Go through this list before releasing an MLOps pipeline.

## Data

- Is the training data pulled as of a date (Training-Serving Skew)?
- Are the schema and range rules written, with a threshold for the share
  of invalid rows?
- Does a rejection send an alert?

## Training and the gate

- Is training done with a fixed seed and fixed library versions?
- Is the gate's set current, labelled and separate from the training data?
- Must the candidate beat the live model by at least `MIN_GAIN`?
- If the gate's set comes from the same source as the training data, is
  that source validated too?

## Registry and release

- Is every version in the registry with its data digest, measurements and
  threshold?
- Does a new version go through shadow and canary?
- Is rolling back a single command (a label on the previous version)?

## Monitoring

- Is drift (PSI) measured every day, and accuracy when the labels arrive?
- Are the calibration gap and the business measure monitored?
- Are the trigger thresholds (`MAX_DROP`, `MAX_DRIFT`) written with names?

## The lesson's thresholds

| Name | Value | Meaning |
|---|---|---|
| `MAX_DROP` | 0.05 | A drop this large from the gate score triggers retraining |
| `MAX_DRIFT` | 0.25 | A trigger if one column's PSI exceeds this |
| `MAX_INVALID` | 0.05 | A rejection if the share of invalid rows in the window exceeds this |
| `MIN_GAIN` | 0.003 | The candidate stays out unless it is at least this much better |
