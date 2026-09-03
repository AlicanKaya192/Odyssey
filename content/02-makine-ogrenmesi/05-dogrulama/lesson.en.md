# Validation and Overfitting

In every section so far we measured a single number: the error on the test
set. This section asks **how much that number can be trusted**.

There are two questions and they lead to the same place:

- Is the model memorising or learning?
- Is the number I measured real, or a piece of luck?

## Two scores, four situations

Since section 1 we have looked only at the test score. Put the training
score beside it and a great deal more about the model becomes visible.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Overfitting</h4>
      <p>Training <b>excellent</b>, test <b>poor</b>.<br>The model memorised; it never derived the rule.</p>
    </div>
    <div class="versus-side">
      <h4>Underfitting</h4>
      <p>Both <b>poor</b>.<br>The rule stayed too simple.</p>
    </div>
  </div>
  <figcaption>The test score alone cannot tell these apart: 62% can come from a model that memorised or from one that learned nothing. The fixes differ.</figcaption>
</figure>

The practical value of the distinction: **the two situations call for
opposite fixes.**

- For overfitting you **simplify** the model or add data.
- For underfitting you **complicate** it or add features.

A wrong diagnosis sends you the wrong way.

## The complexity knob

A decision tree's `max_depth` tunes complexity directly. On the same data,
let us watch both scores as the depth grows:

```
depth   training   test
    1      99.68   96.65
    2      72.72   58.47
    3      51.34   65.30
    5      18.25   53.83
    8       0.19   56.83
 none       0.00   59.06
```

**The training column falls to zero.** With no depth limit the tree
memorises every record in its own branch and makes **no error at all** on
the training data.

**The test column does not fall.** It wanders between 53 and 96 and never
drops below 50.

**The gap between them is overfitting itself.** At depth 1 the difference is
-3.03 (the model is so simple it is equally bad on both); with no limit it
is **59.06**.

A training error of zero is not something to celebrate; that number says the
model memorised the data, not that it learned.

## Look carefully at the test column

Now the real issue. The test column runs:

```
96.65 → 58.47 → 65.30 → 53.83 → 56.83 → 59.06
```

58.47 at depth 2, 65.30 at 3, 53.83 at 5. **Not a smooth curve — it jumps.**

Which depth is best? Reading the table and saying "5" is easy. But on a test
set of 27 records, are the five-unit gaps between these numbers a real
advantage, or an accident of which 27 cars landed in the test set?

Choosing a depth without answering that means deciding on noise.

## How lucky is a single split

Let us try: the same model, the same data, only `random_state` changes.

```
random_state    0      1      2      3      4
MAE          16.16  16.95  17.07  19.68  21.56
```

**The lowest is 16.16, the highest 21.56.** A spread of **5.40** — about a
third of the number itself.

The model did not change. The data did not change. The only thing that
changed is which 27 cars fell into the test set.

This is a warning that sits above every number we measured in earlier
sections: **a result from a single split is an estimate, not a precise
measurement.** Writing `random_state=42` makes the result reproducible; it
does not make it more accurate.

## Cross validation

The fix is simple: measure not once but **many times**, and average.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">round 1</span><span class="anat-body">the data is cut into five; <b>piece 1 is the test</b>, the other four train</span></div>
    <div class="anat-row"><span class="anat-label">round 2</span><span class="anat-body"><b>piece 2 is the test</b>, the other four train</span></div>
    <div class="anat-row"><span class="anat-label">…</span><span class="anat-body">each piece takes its turn as the test exactly once</span></div>
    <div class="anat-row"><span class="anat-label">result</span><span class="anat-body">the <b>mean</b> of the five scores and their <b>spread</b></span></div>
  </div>
  <figcaption>Every record is tested exactly once and used for training exactly four times. No data goes to waste.</figcaption>
</figure>

```python
from sklearn.model_selection import KFold, cross_val_score

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf,
                         scoring="neg_mean_absolute_error")
```

```
fold scores: [14.97, 15.96, 19.29, 19.63, 12.64]
mean 16.50   spread (std) 2.65
```

**Two numbers come out, and the second is worth at least as much as the
first.**

- **16.50** is the model's expected error.
- **2.65** is how much that number moves.

A large spread means you should trust the number less. If two models have
means of 16.5 and 17.2 with spreads of 2.65, the 0.7 between them means
nothing.

**The `neg_` prefix looks odd but has a reason:** sklearn treats every score
as "larger is better". For an error that is backwards, so the sign is
flipped. The results come back negative and you read them with a minus in
front.

**`shuffle=True` is usually needed:** if the file is sorted on a column,
cutting without shuffling makes the folds very different from one another.

## What to look at where: three pieces

Where does cross validation sit? For that you need to remember that data has
three jobs.

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Training</b><br>the model learns</span>
    <span class="arrow">+</span>
    <span class="node"><b>Validation</b><br>settings are chosen</span>
    <span class="arrow">+</span>
    <span class="node ok"><b>Test</b><br>measured once</span>
  </div>
  <figcaption>Choosing a setting by looking at the test set turns the test into training data. The third box is opened once, at the very end.</figcaption>
</figure>

With plenty of data you split three ways. With little data that is
expensive: cut 106 rows into three and every piece is tiny.

**Cross validation takes the validation set's place.** The training side is
split and measured over and over while the test set waits untouched.

The order:

1. Split the data into training and test. Put the test aside.
2. Choose the settings **on the training side, with cross validation**.
3. Train the model with those settings on all the training data.
4. Measure **once** on the test set and report that number.

## The learning curve: would more data help?

When a model is not good enough there are two routes: **more data** or **a
better model**. The learning curve tells you which will work.

We train the model again and again on growing portions of the training data:

```
records   training   test
     10      10.10   19.40
     20      11.80   18.59
     30      13.87   18.22
     45      15.45   18.01
     60      16.33   16.75
     79      15.52   15.69
```

**The two curves move towards each other.** The training error **rises**
(memorising 10 records is easy, 79 is not), the test error **falls**, and in
the end they meet: 15.52 and 15.69.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>If the curves have met</h4>
      <p>More data <b>will not help</b>.<br>What you need: a new feature or a different model.</p>
    </div>
    <div class="versus-side">
      <h4>If a gap remains</h4>
      <p>The model is memorising.<br>More data <b>will help</b>.</p>
    </div>
  </div>
  <figcaption>A learning curve lets you measure "should I collect data or change the model" instead of guessing.</figcaption>
</figure>

The answer here is clear: the two curves met, so this model has taken what
this data has to give. Collecting a hundred more cars will not change the
result.

## A complex model is not a better model

This section's quiet finding. Measured on the same data with cross
validation:

```
decision tree (depth 5)   MAE 64.33
decision tree (no limit)  MAE 66.21
linear regression         MAE 16.50
```

**The tree is not even a quarter as good as a straight line.**

The reason is simple: in this data the price really is **linearly** related
to area, age and mileage. Linear regression captures that relationship
exactly; the tree tries to imitate it in steps and cannot build enough steps
from 106 rows.

The lesson: **choosing a model is not a matter of fashion but of
measurement.** More complex does not mean better.

## What we skipped in this section

- **Automating the search for settings.** Instead of writing a loop by hand,
  `GridSearchCV` tries every combination with cross validation and picks the
  best. It arrives in section 11.
- **Folds in classification.** When the classes are imbalanced,
  `StratifiedKFold` is used instead of `KFold`: each fold keeps the class
  proportions.
- **Time series.** There a random fold leaks the future into the past;
  `TimeSeriesSplit` is needed.

For now you have two habits: **look at both scores** and **do not trust a
number from a single split too far.** Both hold in every section that
follows.
