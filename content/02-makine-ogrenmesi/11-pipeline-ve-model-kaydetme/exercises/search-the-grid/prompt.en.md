A pipeline works directly with `GridSearchCV` — and not only the model's
settings but the **preprocessing's** can be searched too.

**What you need to do:**

1. Prepare, split the data and build the pipeline
   (`LogisticRegression(max_iter=1000)`).
2. Set up a `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
3. Define a two-parameter grid:
   - `prepare__num__impute__strategy`: `["median", "mean"]`
   - `model__C`: `[0.01, 0.1, 1, 10]`
4. Search with `GridSearchCV` (`scoring="accuracy"`). Print one line per
   point: **the strategy, C, the CV mean** (three decimals).
5. Print the best settings (strategy and C) and that setting's CV score.
6. On the last line print **the search's test accuracy** and **the untuned
   pipeline's test accuracy** side by side.

**Expected output:**

```
median 0.01 0.711
mean 0.01 0.704
median 0.1 0.74
mean 0.1 0.74
median 1 0.738
mean 1 0.744
median 10 0.736
mean 10 0.736
mean 1 0.744
0.793 0.793
```

**The grid's key format is the most confusing thing in this section:**

```
prepare__num__impute__strategy
   |     |      |        |
   |     |      |        +-- SimpleImputer's parameter
   |     |      +----------- the step inside the ColumnTransformer
   |     +------------------ the ColumnTransformer's part
   +------------------------ the step in the Pipeline
```

Every level is separated by **two underscores**. Write a single one and
`GridSearchCV` says there is no such parameter.

**The imputation strategy is now a hyperparameter.** You used to think
"median or mean?" and pick one; now you measure.

**As for the result — this is the honest part.**

The best setting is `mean` with `C=1`, at a CV score of 0.744. The default
(`median`, `C=1`) gives 0.738. **A gain of 0.006.**

**The last line is even plainer: 0.793 and 0.793.** The setting the search
chose gives **exactly the same** test score as the untuned pipeline.

So eight points were searched, forty models were trained, and **nothing
changed.**

**That is not a failure but information.** On this data neither `C` nor the
imputation strategy matters; improvement has to come from somewhere else —
more data, better features, or a different model. You could not have known
that without measuring.

**And a warning:** `best_score_` (0.744) is not the final report. That
number comes from cross validation on the training side and is optimistic
**because the best of eight points was chosen.** The final report is on the
test set: 0.793.
