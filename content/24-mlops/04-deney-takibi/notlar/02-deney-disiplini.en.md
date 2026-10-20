Keeping records is not enough; you also need to make the right decision
with them.

## The winner's curse

When many candidates are measured on the same data and the best one is
picked, the chosen one's score looks higher than it really is. The
lesson's measurement:

| | Validation | Test |
|---|---|---|
| The best of 20 identical models, ahead of the average by | +0.028 | +0.009 |

The models differed only by their seed; most of the lead on validation
vanished on new data. The more experiments, the bigger this optimism.

## Rules

- Choose with **validation**, report with **test**.
- Don't look at the test set before choosing. The moment you look, the
  test turns into validation.
- Keep the number of experiments in the record: "the best of 200
  attempts" and "the best of 3 attempts" don't deserve the same trust.
- Record bad results too; what didn't work is information as well.
- Always record the baseline.
- Let two experiments differ in **one thing only**; if two things change
  at once, you can't tell which one worked.

## Their counterparts in real tools

| In this section | MLflow |
|---|---|
| `log_run(params, metrics)` | `mlflow.log_param(...)`, `mlflow.log_metric(...)` |
| `runs.jsonl` | The `mlruns/` folder or a tracking server |
| The sorted table | The `mlflow ui` web interface |
| The experiment number | The run ID |

## Checklist

- Is every experiment recorded on its own from inside the code, not by
  hand?
- Are all the settings in the record? (A setting not in the record means
  an experiment that can't be reproduced.)
- Was the test set never used for choosing?
- Is the reported number the test result?

## Don't

- Don't change or delete old lines in the log file.
- Don't record only the best result.
- Don't compare experiments on different splits; the luck of the split
  mixes into the difference.
