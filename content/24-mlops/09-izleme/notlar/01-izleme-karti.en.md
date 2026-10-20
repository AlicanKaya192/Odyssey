| Layer | Measure | When | Example threshold |
|---|---|---|---|
| System | p95 latency | At once | Above 200 ms |
| System | Error rate (`5xx`) | At once | Above 1% |
| Input | Column mean | At once | Clearly far from training |
| Input | Requests breaking the schema (`422`) | At once | Above 2% |
| Prediction | "Will leave" rate | At once | 0.1 away from the start, two months in a row |
| Quality | Accuracy | When the labels arrive | Below 0.75 |

## The lesson's eight months

| Month | Predicted rate | Usage | Accuracy |
|---|---|---|---|
| 0 | 0.204 | 32.0 | 0.813 |
| 3 | 0.390 | 27.5 | 0.784 |
| 4 | 0.498 | 25.0 | 0.673 |
| 7 | 0.590 | 21.5 | 0.658 |

The predicted rate alert went off in month 3; accuracy dropped in month
4, and that could only be known in month 5.

## What is in the prediction log?

| Field | Why |
|---|---|
| Customer ID | To join with the real outcome |
| Time (month, day) | To group by time |
| Model version | Quality version by version |
| Prediction (probability) | To watch the distribution and compute accuracy |
| Inputs (or a sample of them) | To catch training-serving skew |

## Terms

- **Monitoring:** continuously measuring the health of the model in
  production.
- **Prediction log:** a record where every prediction is written with the
  ID, version and time.
- **Delayed label:** the real outcome arriving after the prediction, late.
- **Alert fatigue:** alerts that go off too often being ignored.
