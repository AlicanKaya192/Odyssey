The last exercise. Tune the model, save it, load it back and produce
predictions from **raw patient records**.

**What you need to do:**

1. Prepare and split the data (no `followup_calls`, `stratify=y`).
2. Build the pipeline: the preprocessor +
   `LogisticRegression(max_iter=1000, class_weight="balanced")`.
3. Search with `GridSearchCV` (`StratifiedKFold` 5 folds, `shuffle=True`,
   `random_state=42`, `scoring="average_precision"`):
   - `model__C`: `[0.01, 0.1, 1, 10]`
   - `prepare__num__impute__strategy`: `["median", "mean"]`
4. Print the best `C`, the best strategy and the CV score on one line.
5. Save the best pipeline as `model.joblib`; print that the file is larger
   than 1000 bytes.
6. Load it back. Print the average precision on the test set.
7. Build a `DataFrame` of three new patients:
   - 72 / male / south / bmi 34.5 / visits 5 / smoker yes
   - 29 / female / **unknown region** / **unknown bmi** / visits 0 /
     smoker no
   - 58 / female / north / bmi 26.0 / visits 2 / smoker no
8. Print the three patients' probabilities (three decimals).
9. On the last line print the predictions produced **with a 0.3 threshold**.

**Expected output:**

```
0.01 median 0.541
True
0.444
[0.825, 0.234, 0.426]
[1, 0, 1]
```

**The first line: `C=0.01` and `median`, at a CV score of 0.541.** All eight
points sit between 0.533 and 0.541; the untuned setting (`C=1`, `median`)
gives 0.534. **A gain of 0.007 against a spread of 0.031** — so the search
changed nothing in practice.

That is not a failure but information: on this data neither `C` nor the
imputation strategy matters. Improvement has to come from somewhere else.

**The second and third lines:** the model was saved, loaded back, and gave
0.444 on the test set.

**The fourth line is the real test.** The second patient's `bmi` and
`region` are empty. You handed it a raw dict — unscaled numbers, unencoded
text, missing values.

The model worked, because what was saved is not the coefficients but **the
whole pipeline**: the median computed during training, the mode, the
encoder's categories, the scaling values and the column order.

**The probabilities read plainly:**

- The first patient at **0.825** — 72 years old, a smoker, BMI 34.5, five
  visits. Four risk factors at once.
- The second at **0.234** — 29 years old, non-smoker, no visits. The two
  missing columns were filled with the median and mode learned during
  training.
- The third at **0.426** — in the middle, and undecided.

**The last line is what the threshold does.** Had you called `predict()` it
would use 0.5 and the result would be `[1, 0, 0]`. **With a 0.3 threshold
the third patient turns into a 1 as well**: `[1, 0, 1]`.

The same model, the same probabilities, a different decision — and the only
thing that made it was writing 0.3 instead of 0.5.

That threshold is **not** in the `joblib` file. `predict()` always uses 0.5.
If you do not note the threshold you chose, the next person to use the
model will silently run a different one.

**This is exactly why a note sits beside the file** — the second note
explains how to write it.

You are at the end of the module. You know how to build a model, measure it
honestly, protect it from leakage and ship it.
