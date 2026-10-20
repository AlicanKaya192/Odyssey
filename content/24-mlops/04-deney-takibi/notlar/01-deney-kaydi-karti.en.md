What an experiment record should hold:

| Field | Example | Why |
|---|---|---|
| Number | `"run": 3` | To refer to the experiment by name |
| Settings | `{"model": "logistic", "C": 0.1}` | The whole recipe of the experiment |
| Measurements | `{"val_accuracy": 0.832}` | To compare |
| Data fingerprint | `"data": "a91a352912da"` | Which data |
| Code version | The Git commit ID | Which code |
| Note | `"dropped the fee column"` | Why it was tried |

## JSON Lines

```text
{"run": 1, "params": {"model": "baseline"}, "metrics": {"val_accuracy": 0.748}}
{"run": 2, "params": {"model": "logistic", "C": 0.01}, "metrics": {...}}
```

- One line per experiment; every line is valid JSON on its own.
- Writing: open the file in append mode (`open("a")`), write one line at
  the end.
- Reading: `[json.loads(line) for line in text.splitlines()]`.
- Old lines are never changed; if an experiment was wrong, it is
  corrected with a new line.

## Three sets

| Set | What for | When |
|---|---|---|
| Train | Training the model | In every experiment |
| Validation | Comparing and choosing experiments | In every experiment |
| Test | Reporting the chosen model | Once, at the very end |

## The baseline

The simplest guess that learns nothing: telling everyone the most common
class. On this module's data it is 0.748 on the validation
set. Every model must beat it first.

## Terms

- **Experiment tracking:** recording the settings and results of every
  attempt on its own.
- **Run:** one training and measurement with one set of settings.
- **Baseline:** the simplest result the models must beat.
- **JSON Lines:** a file format where every line is a separate JSON.
