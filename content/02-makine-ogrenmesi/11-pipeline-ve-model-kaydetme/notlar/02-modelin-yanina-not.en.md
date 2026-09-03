`joblib.dump` produces a file, and that file is **half** the model. The
other half is the note written beside it.

Without that note, six months later you are left with a binary file called
`model.joblib` and no idea what it does.

## What is not saved

| | |
|---|---|
| **In the file** | Every step, the learned median/mode/mean, the encoder's categories, the model's coefficients, the column order |
| **Not in the file** | The library versions |
| **Not in the file** | The training data and where it came from |
| **Not in the file** | The decision threshold you chose |
| **Not in the file** | The scores you measured and on which test set |
| **Not in the file** | What you deliberately left out |

The last row is often skipped and is the most expensive. Nobody remembers
the answer to "why didn't we use the `age` column?" six months later.

## A sufficient note

A plain text file placed beside the model. An example:

```
model.joblib
============
What it does : subscriber churn prediction, binary classification
Trained on   : subscribers.csv, 600 rows, the 2026-09 copy
Input        : city, plan (text) + tenure, monthly, support (numeric)
               raw data is passed in; the pipeline fills the gaps
Output       : 0 = stays, 1 = leaves

Measured     : baseline 0.573
               cross validation 0.738 +/- 0.037 (5 folds, training side)
               test accuracy 0.793 (150 records, measured once)

Threshold    : 0.5 (the default; the business gave no cost figures)
Settings     : LogisticRegression(C=0.1), chosen by GridSearchCV

Left out     : customer id (an identifier, nothing to learn)
               signup date (carries the same information as tenure)

Environment  : scikit-learn 1.7, pandas 3.0, Python 3.14
               the detail is in requirements.txt

Known limits:
  - few examples for cities other than Bursa
  - not tested against data from before 2026
```

Twenty lines. Five minutes to write, a day to be without.

## Version compatibility

A `joblib` file stores Python objects. Opening it under a different
scikit-learn version can:

- **Work** (a small version gap, with a warning)
- **Warn and work incorrectly** (if the internals changed)
- **Not open at all** (if a class was removed)

This is why a `requirements.txt` sits beside the model:

```
scikit-learn==1.7.0
pandas==3.0.5
numpy==2.3.0
```

Ignoring the warning is a common mistake. `InconsistentVersionWarning` does
not say "probably fine"; it says "check".

## The threshold is not in the file

In section 09 you measured that lowering the threshold from 0.5 to 0.1
raised the frauds caught from 6 to 13.

**That threshold does not go into the `joblib` file.** `predict()` always
uses 0.5. The threshold you chose lives only in your own code:

```python
probability = loaded.predict_proba(new)[:, 1]
prediction = (probability >= 0.1).astype(int)
```

If you do not note it, the next person to use the model calls `predict()`
and **silently runs a different model.**

## Models age

Production data drifts away from the training data over time: prices
change, a new city opens, customer behaviour shifts. The model stays the
same and **quietly gets worse.**

This is called **drift**, and it comes in two kinds:

| Kind | What changes | Example |
|---|---|---|
| Data drift | The distribution of the inputs | The average subscription fee doubles |
| Concept drift | The input-target relationship | A competitor appears and cheap plans start churning too |

The second is sneakier: the inputs look the same, but the model is now
wrong.

**What is done in practice:**

- The distribution of the predictions is monitored (if it suddenly says
  "leaves" to everyone, something happened).
- The score is remeasured as real outcomes arrive.
- The model is retrained at regular intervals and **compared with the old
  one.**

That last point matters: a new model is not always better.

## While producing the file

- **Put a version in the name:** `churn-2026-09.joblib`. `model.joblib`
  becomes confusing by the third model.
- **Keep the training script.** Being able to reproduce the model is worth
  more than keeping the file.
- **Fix the random seed.** Without `random_state` the same script does not
  give the same model.
- **Measure the test score once.** If you look at the test set a second
  time and change a setting, that score is no longer honest.

## In one sentence

**The saved file does not say what the model does; the note beside it
does.**
