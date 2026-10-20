The module's rules, measures and thresholds on a single page.

## Thresholds and measures

| What | Rule | Section |
|---|---|---|
| PSI | Below 0.1 stable, above 0.25 a large drift | 10 |
| Noise | The value of another sample from the same period | 10, 12 |
| The gate | The candidate must beat the live model by `min_gain` on the same current set | 5, 11 |
| Calibration | The mean probability and the actual rate should be close | 11 |
| Latency | Written with p95; the mean hides the tail | 7, 13 |
| Utilization | Planned with headroom, not for 100% (e.g. 70%) | 13 |
| A/A noise | Drops to about half when the group grows four times | 12 |

## What should a record hold?

| Record | Contents |
|---|---|
| Training record | Seed, settings, the data's digest, library versions |
| Experiment record | Every experiment, the bad ones too: settings, validation score |
| Model registry | Version, file digest, measurements, threshold, live label, model card |
| Prediction log | Id, model version, prediction, inputs; later the actual outcome |

## Common mistakes

| Mistake | Result | Section |
|---|---|---|
| Choosing the seed by the result | An optimistic measurement | 1, 4 |
| Training without checking the data | The code runs, the model breaks | 2 |
| Choosing on test and reporting on test | The winner's curse | 4 |
| Separate feature code for training and serving | Training-serving skew | 8 |
| Tying an alert to the p-value | Everything is "significant" with a large sample | 10 |
| Running the gate with an old set | The new model is unfairly rejected | 11 |
| Deciding on a small canary | Luck decides | 12 |
| Leaving the threshold at 0.5 | A loss in the business measure | 14 |
