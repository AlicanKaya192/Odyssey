# Reproducible Training

Yesterday you trained the model and measured 0.788. Today you ran the
same code again without touching anything and got 0.766. Which one is
right? Did something break? How do you get back to the old result? If
training is not **reproducible**, you cannot answer any of these
questions. In this section we find the things that move the result one
by one and pin them down.

## Same code, different result

Let's train a random forest model three times on the same data. The data
is the same every time: `make_customers(2000)`.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(2000))
for attempt in [1, 2, 3]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    model = RandomForestClassifier(n_estimators=50).fit(X_train, y_train)
    print("attempt", attempt, "accuracy:", round(model.score(X_test, y_test), 3))
```

```text
attempt 1 accuracy: 0.774
attempt 2 accuracy: 0.734
attempt 3 accuracy: 0.784
```

Three attempts, three different results. If you ran this code you would
see three other numbers again. When the code and the data are the same
but the result changes, there is **randomness** involved.

## Where does the randomness come from?

Two places in the code above behave randomly:

- **`train_test_split`** shuffles the rows before splitting them. On
  every run, other customers land in the test set.
- **`RandomForestClassifier`** builds each tree from randomly chosen rows
  and, at each split, from randomly chosen columns.

Many other methods use randomness too: k-means picks its starting centres
at random, and a neural network starts its weights from random values.
Randomness on a computer is really **pseudo-random**: a sequence of
numbers computed from a starting number, the **seed**. With the same
seed, the sequence is the same.

## Fixing the seed

In scikit-learn the seed is given with the `random_state` parameter.
Let's give a seed to both random steps:

```python
for attempt in [1, 2, 3]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0)
    model = RandomForestClassifier(n_estimators=50, random_state=0)
    model.fit(X_train, y_train)
    print("attempt", attempt, "accuracy:", round(model.score(X_test, y_test), 3))
```

```text
attempt 1 accuracy: 0.768
attempt 2 accuracy: 0.768
attempt 3 accuracy: 0.768
```

The three attempts are now exactly the same. If you ran this code you
would see the same number.

One rule when giving the seed: **give each random step its own seed.**
Writing `random.seed(0)` or `np.random.seed(0)` once at the top of the
program seems to work too, but that single shared generator is used
everywhere in the program. When a new line that draws a random number is
added somewhere, all the numbers after it shift. In Python you can also
build your own generator: `random.Random(0)` gives a generator only you
use.

## The seed is a setting too

With the seed fixed, the result repeats. But how much does the result
move when the seed changes? Let's change the split's seed first and then
the model's seed:

```python
for seed in [0, 1, 2, 3, 4]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=seed)
    model = RandomForestClassifier(n_estimators=50, random_state=0)
    model.fit(X_train, y_train)
    print("split seed", seed, "accuracy:", round(model.score(X_test, y_test), 3))
for seed in [0, 1, 2]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0)
    model = RandomForestClassifier(n_estimators=50, random_state=seed)
    model.fit(X_train, y_train)
    print("model seed", seed, "accuracy:", round(model.score(X_test, y_test), 3))
```

```text
split seed 0 accuracy: 0.768
split seed 1 accuracy: 0.788
split seed 2 accuracy: 0.758
split seed 3 accuracy: 0.786
split seed 4 accuracy: 0.762
model seed 0 accuracy: 0.768
model seed 1 accuracy: 0.768
model seed 2 accuracy: 0.764
```

Changing only the split moved the accuracy between 0.758 and
0.788. The effect of the model's seed is much smaller. Two
lessons follow from this:

- **Compare two models on the same split.** If one is measured on one
  split and the other on another, part of the difference is pure luck.
- **Don't choose the seed by the result.** Trying five seeds and
  reporting the best one makes the model look better than it is. The
  seed is chosen before training and not changed. The way out of the
  luck of a single split is cross-validation: the average over many
  splits.

## All settings in one place

If everything that affects the result, that is the size of the data,
the seeds and the model's settings, sits as constants scattered through
the code, it is easy to change one and forget to record it. Let's collect
them all in one dictionary, a **configuration** (config for short). The
training function looks only at this dictionary:

```python
import json

CONFIG = {"rows": 2000, "data_seed": 7, "split_seed": 0,
          "n_estimators": 50, "model_seed": 0}


def train(config):
    X, y = to_xy(make_customers(config["rows"], seed=config["data_seed"]))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=config["split_seed"])
    model = RandomForestClassifier(n_estimators=config["n_estimators"],
                                   random_state=config["model_seed"])
    model.fit(X_train, y_train)
    return model, round(model.score(X_test, y_test), 3)


model, accuracy = train(CONFIG)
print("accuracy:", accuracy)
print(json.dumps(CONFIG, indent=2))
```

```text
accuracy: 0.768
{
  "rows": 2000,
  "data_seed": 7,
  "split_seed": 0,
  "n_estimators": 50,
  "model_seed": 0
}
```

Now the answer to "how was this model trained?" is a dictionary. The
dictionary can be written to a file as JSON and kept next to the model;
calling `train` again with the same dictionary produces the same model.
In real projects the configuration usually lives in a separate YAML or
JSON file that is read apart from the code.

## Knowing the data by its fingerprint

The configuration pins down the code's settings. What about the data?
In this module the data is produced from a seed, but in a real project
it comes from a table that changes every day. A file name is not enough
to answer "which data was the model trained on?": the contents of a file
with the same name may have changed.

The answer is to compute a **hash** from the data's contents. A hash
function such as SHA-256 turns data of any length into a text of fixed
length; when a single value changes, the whole hash changes. That is why
the hash is called the data's **fingerprint**:

```python
import hashlib


def fingerprint(rows):
    text = json.dumps(rows, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


rows = make_customers(2000)
print("data:", fingerprint(rows))
rows[0]["tenure"] = rows[0]["tenure"] + 1
print("one value changed:", fingerprint(rows))
print("again from the seed:", fingerprint(make_customers(2000)))
```

```text
data: a91a352912da
one value changed: 7de66b6647f6
again from the seed: a91a352912da
```

When a single value of one of the 2000 customers changed, the fingerprint
changed completely; the data produced again from the same seed gave the
same fingerprint. `sort_keys=True` puts the dictionaries' keys in order,
so the same data does not look different just because its keys were
written in another order. The full hash is 64 characters; the first 12
are enough here.

## The environment: library versions

Even with the same code, settings and data, another version of
scikit-learn can give another result: a default value may have changed,
a calculation may have been corrected. As you saw in the Machine Learning
Libraries module, opening a model saved with one version in another
version can cause trouble too. So two things are done:

- In `requirements.txt` the versions are pinned with `==`
  (`scikit-learn==1.9.1`). The clean machine from the CI/CD and DevOps
  module installs the same versions.
- The versions are written into the training record too.

## The run record

Now let's put it all together. A training run's **record** holds
everything needed to reproduce that run:

```python
import sys
import sklearn

record = {
    "config": CONFIG,
    "data": fingerprint(make_customers(CONFIG["rows"], seed=CONFIG["data_seed"])),
    "python": sys.version.split()[0],
    "scikit-learn": sklearn.__version__,
    "accuracy": accuracy,
}
print(json.dumps(record, indent=2))
```

```text
{
  "config": {
    "rows": 2000,
    "data_seed": 7,
    "split_seed": 0,
    "n_estimators": 50,
    "model_seed": 0
  },
  "data": "a91a352912da",
  "python": "3.14.7",
  "scikit-learn": "1.9.1",
  "accuracy": 0.768
}
```

If someone asks "where did this model come from?" six months later, the
answer is in this record: which settings, which data, which environment
and the measured result. In the Experiment Tracking section we build a
small tool that stores and compares these records.

## Testing reproducibility

It is easy to forget a seed; a newly added step may be left without one.
The way to catch this is to write a **test**, as in the CI/CD and DevOps
module: train twice with the same configuration and compare the two
models' predictions.

```python
model_a, _ = train(CONFIG)
model_b, _ = train(CONFIG)
X_check, _ = to_xy(make_customers(500, seed=99))
same = (model_a.predict_proba(X_check) == model_b.predict_proba(X_check)).all()
print("same predictions:", same)
```

```text
same predictions: True
```

We compare the **predictions**, not the accuracy: two different models
can give the same accuracy by chance, but if they give the same
probability for all 500 customers, they are the same model. If this test
is in the pipeline, the day a step without a seed is added the pipeline
turns red.

## Summary

- Getting a different result with the same code and data comes from
  **randomness**: the shuffle in the split, the random choices inside
  the model.
- Randomness is computed from a **seed**. In scikit-learn it is
  `random_state`; give each random step its own seed.
- The split's seed can move the result much more than the model's seed.
  Compare models on the same split; don't choose the seed by the result.
- Collect every setting that affects the result in one **configuration**.
- The data's **fingerprint** (the hash of its contents) says exactly
  which data was used.
- Pin the library versions and write them into the **run record**.
- Test reproducibility: two trainings with the same settings, the same
  predictions.
