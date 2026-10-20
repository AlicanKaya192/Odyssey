The forms of training-serving skew:

| Form | Example | How to prevent it |
|---|---|---|
| Code skew | The serving team rewrote the feature code and two columns swapped | Feature code in one place; both import it |
| Unit skew | 29.90 in training, 2990 (cents) in production | Schema and a serving-time profile |
| Missing-value skew | Filled with the mean in training, with 0 in production | Filling is part of the feature code too |
| Point-in-time leakage | Calls made while cancelling were counted in training | Features as of the prediction time |
| Data-source skew | A daily batch table in training, another service in production | A feature store with one definition |

## The lesson's measurement

| Situation | Accuracy |
|---|---|
| With the training features | 0.813 |
| Serving code with two columns swapped | 0.297 |
| "Stays" for everyone (the baseline) | 0.703 |
| The leaky model, on the test | 0.939 |
| The leaky model, in production | 0.787 |

The leaky model is the best on the test and worse than the one without
the leak in production.

## Catching it

- At serving time, the vector going into the model is recorded (a sample
  is enough).
- The column means of the recorded vectors are compared with those in
  training.
- If there is a big difference, suspect code skew first: column order,
  unit, filling.

## Terms

- **Training-serving skew:** the model seeing inputs in production that
  were computed differently from training.
- **Point-in-time leakage:** using in training information that couldn't
  be known at prediction time.
- **As-of query:** taking the last value known on a date.
