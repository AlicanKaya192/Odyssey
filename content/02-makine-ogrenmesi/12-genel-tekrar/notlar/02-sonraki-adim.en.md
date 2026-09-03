This module covered scikit-learn's classical machine learning side. What
follows is the answer to "what should I learn now", in order.

## First: build a project

Before learning another library, do something with **your own data**.
Nothing that works only on course data teaches anything:

- Find the data yourself. Kaggle, open government data, the step counter on
  your own phone — it does not matter.
- **Frame the question yourself.** In this module the target column arrived
  ready; in real life "what are we predicting" is the hardest decision.
- Start from the baseline and write your report as though someone else will
  read it.

**The test of what you learned is this:** if your model cannot beat the
baseline, can you say so?

## Time series

Everything in this module assumed the rows are **independent**. On
sequential data that is not true.

- `train_test_split` is **wrong**: splitting at random shows the model the
  future. Time-based splitting is needed.
- `TimeSeriesSplit` is cross validation's time-aware form: each fold trains
  on the past and validates on the future.
- Lagged features, moving averages and seasonality are a subject of their
  own.
- Libraries: `statsmodels`, `prophet`, `sktime`.

**This is the most practical next step after this module**, because most
real data is dated.

## Text

To hand a sentence to a model it has to become numbers.

- `TfidfVectorizer` to start: based on word counts, fast, and it goes
  straight into a `Pipeline`.
- Embeddings after: vectors that place words by meaning.
- Sentiment analysis and topic classification are doable with
  `scikit-learn`; beyond that is deep learning.

## Deep learning

Images, audio and long text stayed outside this module. Neural networks are
a field of their own.

- `torch` (PyTorch) is the de facto standard.
- On tabular data it is **usually unnecessary** — gradient boosting is
  often better and much faster. This is a common mistake.
- On images and text there is no alternative.

**Order matters:** skipping this module to start with deep learning means
building models without the concepts of a baseline or leakage.

## Model explanation

In section 07 you saw feature importance and its three traps. What follows:

- `permutation_importance` — shuffles a column and sees how far the score
  falls; it can be measured on the test set. It is inside sklearn.
- **SHAP** — explains each prediction individually: "why did this patient
  come out high risk?" A separate package.
- Partial dependence plots (`PartialDependenceDisplay`) — draw how the
  prediction changes as one column changes.

When you have to explain a model to someone, these tools become mandatory.

## Shipping to production (MLOps)

Putting the saved file somewhere and running it is its own field:

- Serving: an HTTP endpoint with `FastAPI`.
- Versioning: which model, on which data, trained when.
- Monitoring: the distribution of the predictions, and the score as real
  outcomes arrive.
- Retraining: at regular intervals, and **compared with the old model**.

These are software engineering rather than machine learning, but they are
what makes a model useful.

## Four traps while learning

**1. Collecting libraries.** Learning XGBoost, LightGBM and CatBoost is not
learning something new — all three are gradient boosting. The concepts you
learned here are the same in all of them.

**2. Chasing scores.** Kaggle competitions chase 0.001 improvements; in real
projects that gap changes nothing. Most of the time goes into understanding
the data.

**3. Skipping the baseline.** The most common and most expensive mistake.
Keeping this habit is worth more than learning another library.

**4. Mistaking a model for a cause.** A model finds correlation. "Churn
rises as support calls rise" is true; "reducing support calls will reduce
churn" **may be false**. Finding causes is experiment design.

## Resources

- **scikit-learn's own documentation** — the user guide reads like a course
  and is free.
- **Your own notes.** Every section of this module has a reference note;
  those are your first source.
- **Reading code.** The `sklearn` source is readable; when you wonder what a
  model actually does, you can look.

## Finally

The most valuable thing you learned in this module is not a library but a
habit:

**Do not guess, measure. Never trust one number. Be suspicious of a result
that looks too good.**

Libraries change; those three do not.
