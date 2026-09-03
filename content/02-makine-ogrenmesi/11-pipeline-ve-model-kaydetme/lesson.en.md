# Pipelines and Saving a Model

In section 04 you learned to prepare data for a model: fill the missing
values, encode the text columns, scale the numbers. The rule was one
sentence — **split first, touch afterwards.**

Applying that rule by hand is harder than it looks. This section makes it
**structurally impossible** to break, and then shows how to save the model
to disk.

The data is 600 subscribers: `city`, `plan` (text), `tenure`, `monthly`,
`support` (numbers) and the target `churn`. Three columns have missing
values: `city` 24, `monthly` 48, `support` 30.

## What doing it by hand looks like

The steps needed to hand this data to a model:

```python
# 1. the numeric columns' median (FROM TRAINING)
median = X_train[num].median()
X_train[num] = X_train[num].fillna(median)
X_test[num] = X_test[num].fillna(median)

# 2. the text columns' mode (FROM TRAINING)
mode = X_train[cat].mode().iloc[0]
X_train[cat] = X_train[cat].fillna(mode)
X_test[cat] = X_test[cat].fillna(mode)

# 3. encode the text columns (fit ON TRAINING)
encoder = OneHotEncoder(handle_unknown="ignore")
encoder.fit(X_train[cat])

# 4. scale the numbers (fit ON TRAINING)
scaler = StandardScaler()
scaler.fit(X_train[num])

# 5. join the two
# 6. train the model
```

Six steps, four "from training" warnings and two separate `fit` calls. Now
the real question: **six months from now, when a single new subscriber
arrives, will you be able to repeat those six steps in the same order with
the same numbers?**

Did you write the `median` and `mode` values down anywhere? Did you save
the `encoder` and the `scaler`? Do you remember the column order?

**All of those steps are part of the model.** As long as they live apart,
they are free to get lost, mixed up and leaked.

## The pipeline

`Pipeline` ties those steps into a single object:

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("prepare", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])

pipe.fit(X_train, y_train)
prediction = pipe.predict(X_test)
```

When `fit` is called, every step but the last runs `fit_transform` and the
last runs `fit`. When `predict` is called, every step runs `transform` and
the last runs `predict`.

**The critical point:** on `transform` no step learns again. The median was
computed during training and stayed there.

## Different treatment for different columns

The numeric columns need median + scaling, the text columns mode +
encoding. `ColumnTransformer` does that:

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

numeric = ["tenure", "monthly", "support"]
text = ["city", "plan"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), numeric),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ]), text),
])
```

Two nested `Pipeline`s inside a `ColumnTransformer`. It looks complicated
but reads plainly: **do this to the numeric columns and that to the text
ones.**

The result is a nine-column matrix:

```
num__tenure  num__monthly  num__support
cat__city_Ankara  cat__city_Bursa  cat__city_Izmir
cat__plan_basic   cat__plan_plus   cat__plan_pro
```

Measured: the baseline is 0.573 and the pipeline's test accuracy **0.793.**

**Why `handle_unknown="ignore"` is there:** if a city unseen during
training turns up in the test set, `OneHotEncoder` raises an error by
default. `ignore` sets all that row's city columns to zero. Without this
setting a production model dies on the first unexpected value.

## The real gain: leakage becomes impossible

In section 05 you learned `cross_val_score`. Using it with **hand-prepared**
data is a silent leak:

```python
X_prepared = scaler.fit_transform(X_train)      # it saw all the training data
cross_val_score(model, X_prepared, y_train, cv=skf)
```

The scaler learned the mean of all the training data; then that data was
split into five folds. Each fold's "validation" part consists of rows the
scaler has already seen.

**Given a pipeline, `cross_val_score` retrains every step inside each
fold:**

```python
cross_val_score(pipe, X_train, y_train, cv=skf)
```

This turns leakage from a matter of care into something **structurally
impossible**.

### How much difference it makes

For scaling and imputing the effect is usually small. But it grows when a
step **looks at the target**.

Add 200 **entirely random** columns to the training data and pick the best
15 with `SelectKBest`:

| Where the selection happened | CV accuracy |
|---|---|
| **Outside** the cross validation | **0.780** |
| **Inside** the pipeline | **0.716** |

**A 6.4-point gap, entirely fabricated.** The selector looked at all the
training data and said "these 15 columns resemble the target most"; some of
them were pure noise that happened to resemble the target in that data.
Validated on the same data, they look good.

Inside a pipeline each fold makes its own selection and the trick falls
apart.

**Note:** `train_test_split` is the first defence, from section 04; this is
the second, for **the inside of cross validation**.

## Hyperparameter search

A pipeline works directly with `GridSearchCV`. The step name and the
parameter name are joined by **two underscores**:

```python
from sklearn.model_selection import GridSearchCV

grid = {"model__C": [0.01, 0.1, 1, 10, 100]}
search = GridSearchCV(pipe, grid, cv=skf, scoring="accuracy")
search.fit(X_train, y_train)

print(search.best_params_)   # {'model__C': 0.1}
print(search.best_score_)    # 0.74
```

The measured sweep:

```
C=0.01   0.711
C=0.1    0.740      <- the best
C=1      0.738
C=10     0.736
C=100    0.736
```

`C` is logistic regression's regularisation setting: a small value
constrains the model, a large one frees it. Here the gap between 0.1 and
100 is 0.004 — so on this data `C` barely changes anything. **We learned
that by measuring too.**

**Preprocessing steps can be searched as well:**

```python
grid = {
    "prepare__num__impute__strategy": ["median", "mean"],
    "model__C": [0.1, 1, 10],
}
```

Three levels of underscore: the `strategy` parameter of the `impute` step
inside the `num` part of the `prepare` step. The imputation strategy is now
a hyperparameter.

`search.best_estimator_` gives the pipeline **retrained on all the training
data** with the best settings; `search.predict(...)` uses it directly.

## Saving the model

A trained model lives in memory. When the program closes, it is gone.

```python
import joblib

joblib.dump(pipe, "model.joblib")
loaded = joblib.load("model.joblib")
```

**What gets saved is the whole pipeline:** the medians, the mode, the
categories the encoder learned, the scaler's mean and standard deviation,
the model's coefficients and the column order. All in one file.

The loaded model works on raw data — **even raw data with missing values:**

```python
new = pd.DataFrame([
    {"city": "Bursa", "plan": "basic", "tenure": 3,
     "monthly": 140.0, "support": 4},
    {"city": "Izmir", "plan": "pro", "tenure": 48,
     "monthly": 45.0, "support": 0},
    {"city": None, "plan": "plus", "tenure": 20,
     "monthly": None, "support": 1},
])
print(loaded.predict(new))              # [1 0 0]
print(loaded.predict_proba(new)[:, 1])  # [0.993 0.007 0.466]
```

The third row is missing `city` and `monthly`. The pipeline fills them with
the median and mode it learned during training and produces a prediction:
0.466 — undecided, but working.

**With a hand-prepared model that row would have been a crash.**

## What the saved file does not carry

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-key">Carries</span><span>Every step, the learned numbers, the column order</span></div>
    <div class="anat-row"><span class="anat-key">Does not</span><span>The library versions</span></div>
    <div class="anat-row"><span class="anat-key">Does not</span><span>The training data or where it came from</span></div>
    <div class="anat-row"><span class="anat-key">Does not</span><span>The decision threshold you chose</span></div>
    <div class="anat-row"><span class="anat-key">Does not</span><span>The scores you measured</span></div>
  </div>
  <figcaption>Putting a text file next to it is a favour to the you of six months from now.</figcaption>
</figure>

**Version compatibility is a real problem.** A `joblib` file stores Python
objects; loading it under a different scikit-learn version may warn or may
not work at all. Keeping a `requirements.txt` next to the model should
become a habit.

**`joblib` rather than `pickle`**: it does the same job but is noticeably
faster with large NumPy arrays and produces smaller files.

**A security warning:** `joblib.load` constructs the Python objects inside
the file. A model file from a source you do not trust can run code when
opened. Be careful with anything you did not produce yourself.

## The full flow

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>read and<br>split</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>build the<br>pipeline</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>3</b><br>compare<br>models</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>4</b><br>search the<br>settings</span>
    <span class="arrow">&rarr;</span>
    <span class="node acc"><b>5</b><br>measure once<br>on test</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>6</b><br>save and<br>write the note</span>
  </div>
  <figcaption>Steps three and four stay on the training side; the test set is opened only at step five.</figcaption>
</figure>

## What we left out

- **`RandomizedSearchCV`.** Instead of trying every point of the grid it
  tries a random subset. As the parameter count grows the grid grows
  exponentially; a random search covers far more ground in the same time.
- **`FunctionTransformer` and writing your own step.** Any class with `fit`
  and `transform` methods can go in a pipeline — including your own feature
  engineering code.
- **Serving a model.** Putting the saved file behind an HTTP service,
  versioning it, monitoring it. These are software engineering rather than
  machine learning, and a field of their own (MLOps).
- **Drift.** Production data drifts away from the training data over time
  and the model quietly gets worse. The answer is monitoring and regular
  retraining.

This section in one sentence: **the model is not just the last step; all the
preprocessing is part of the model, which is why they are trained together
and saved together.**
