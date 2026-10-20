The things tested in an ML pipeline and when they fail:

| Test | What it catches | Example |
|---|---|---|
| Unit test | A bug in the feature code | The column order changed |
| Data validation | Broken data | The fee arrived in cents |
| Reproducibility | A new step without a seed | Two trainings give different predictions |
| Floor | General decline | Accuracy below 0.78 |
| Margin over the baseline | A model that learned nothing | Accuracy equal to the baseline |
| Slice bar | A collapse in one group | 0.654 on `pro` customers |
| Directional test | Backwards logic | Churn probability falls as calls grow |
| Obvious example | A big mistake | Thinks a clear churner "stays" |

## The lesson's measurement

| Model | Accuracy | Gate |
|---|---|---|
| Logistic regression | 0.813 | Passed |
| The same with `C=0.0001` | 0.703 (the baseline) | Four problems |

| Model | Customers the directional test held for |
|---|---|
| Logistic regression | 100% |
| Random forest | 95.7% |

## Kinds of behavioral tests

- **Directional:** when a value changes in a certain direction, the
  prediction should move in the expected direction.
- **Invariance:** when something that shouldn't affect the result
  changes, the prediction shouldn't change. For example the customer's
  ID or the spelling of their name.
- **Minimum functionality (obvious examples):** on a few examples whose
  answer everyone knows, the model should be right.

## Terms

- **Quality gate:** a step that compares the model with the bar and stops
  the pipeline if it doesn't pass.
- **Slice:** a part of the data, such as one plan, one city, or new
  customers.
- **Behavioral test:** a test that looks not at the model's accuracy but
  at the logic of its reactions.
