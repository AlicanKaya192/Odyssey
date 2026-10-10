This module showed the daily tools of data science in depth. From here,
several directions open up.

## Next in this path

The **ML Libraries** module covers the whole structure of scikit-learn:
preprocessing, `Pipeline`, cross-validation, model selection, metrics. What
you learned here is used directly there:

- **NumPy arrays** are the model's input and output; broadcasting, scaling
  and `rng` seeds are everywhere.
- **pandas** prepares the data for the model: combining, missing values,
  categories, time features.
- **Charts** are the way to see a model's errors: residuals, the confusion
  matrix, the learning curve.
- **SciPy**'s statistics help compare two models, and its optimisation runs
  inside models.

## Links to other paths

| Path / module | Which part of this module |
|---|---|
| Time Series | pandas time tools, `resample`, `rolling`, `shift` |
| Big Data | pandas performance, types, memory; reading piece by piece |
| ML Algorithms | NumPy and linear algebra: writing models from scratch |
| Mathematics | the meaning of distributions, tests and linear algebra |

## Exploring on your own

- Each library's "User Guide": the official guides of pandas, NumPy,
  matplotlib and SciPy contain many tools not covered in this module.
- matplotlib's example gallery: the fastest way to see how a chart is made.
- Work with your own data: find a CSV, ask, combine, draw, test. Every
  section of this module is a step of that flow.

## A short list of common mistakes

| Mistake | In this module |
|---|---|
| Rows silently vanishing | Combining |
| An operation on the wrong axis | Broadcasting |
| A table that does not change | pandas Performance (Copy-on-Write) |
| A wrongly calculated bar | seaborn |
| Reading too much into p | scipy.stats |
| Forgetting a constraint | scipy.optimize |
