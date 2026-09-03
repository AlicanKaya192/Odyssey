# Ensemble Methods

The previous section ended with a weakness: **a single tree is unstable.**
Remove a few rows from the data and even the root split can change.

This section's idea is surprisingly simple: **build many trees, ask them
all, follow the majority.**

## First, let us measure the instability

Take out a different 10% of the training data each time and retrain the
tree:

```
tree test scores : [0.92, 0.88, 0.78, 0.80, 0.80, 0.84]
root threshold   : [16.5, 15.5, 16.5, 18.5, 28.5, 18.5]
```

**The score wanders between 0.78 and 0.92** — a 14-point range. The same
data, the same model; all that changed is which rows dropped out.

The second line is more troubling: **the root split's threshold climbs from
15.5 to 28.5.** So the model's rule changes too. Yesterday it said "those
who visit fewer than 16 times a month"; today it says "fewer than 28".

The same experiment with a forest:

```
forest test scores: [0.90, 0.84, 0.86, 0.90, 0.90, 0.92]
```

**An 8-point range instead of 14.** The same noise, damped by half.

## The idea: bagging

<figure class="fig">
  <div class="flow">
    <span class="node"><b>Training data</b></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>N random samples</b><br>each a different set of rows</span>
    <span class="arrow">→</span>
    <span class="node"><b>N trees</b><br>each on its own sample</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Majority vote</b></span>
  </div>
  <figcaption>Each tree sees the data slightly differently and so errs slightly differently. Averaged, the errors cancel out.</figcaption>
</figure>

The samples are drawn **with replacement**: the same row can appear twice in
one sample and not at all in another. This is called **bootstrap**, and the
name "bagging" comes from it (bootstrap aggregating).

**Why it works:** a single tree's error is largely **random** — this row
dropped so the threshold moved, that row entered so a branch changed. Random
errors cancel when averaged. Systematic errors do not, but those are a
question of model choice.

## Random forest

A random forest adds **a second randomness** to bagging: at each split it
tries not all the features but **a randomly chosen subset**.

That looks strange — why deliberately handicap the model?

Because without the handicap all the trees **look alike**. If the data has
one very strong feature, every tree picks it at the root and there is no
diversity left to average. Hiding features makes the trees differ from one
another.

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
```

**Scaling is still unnecessary** — everything inside is a tree.

## How many trees

```
trees   training   test
    1      0.947   0.720
    5      0.993   0.840
   25      1.000   0.900
  100      1.000   0.900
  300      1.000   0.900
```

**One tree gives 0.72, twenty-five give 0.90.** Then it flattens: 100 and
300 trees give the same result.

**The most important thing here is what does not happen:** adding trees does
not cause overfitting. The training accuracy stays at 1.000 while the test
accuracy **does not fall**. Because each tree memorises different things,
the average stays clean.

So `n_estimators` is not a balance parameter but a **cost** parameter: more
trees means slower, and past a point not better. Somewhere between 100 and
300 is a common starting point.

## Boosting: a different idea

In a forest the trees are **parallel** and unaware of one another. In
boosting they are built **in sequence**, and each new tree focuses on where
the previous ones **got it wrong**.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Forest (bagging)</h4>
      <p>Trees in parallel, independent.<br>Aim: <b>reduce variance</b>.<br>The trees are deep and strong.</p>
    </div>
    <div class="versus-side">
      <h4>Boosting</h4>
      <p>Trees in sequence, correcting each other.<br>Aim: <b>reduce bias</b>.<br>The trees are shallow and weak.</p>
    </div>
  </div>
  <figcaption>One says "average enough good guesses and the noise dies"; the other says "reduce what error is left, a little at each step".</figcaption>
</figure>

```python
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(random_state=42)
```

Boosting's critical setting is `learning_rate`: how much each tree
contributes to the correction. A small value is safer but needs more trees.
It is tuned together with `n_estimators`.

**Boosting can overfit** — unlike a forest. Past a point, adding trees
lowers the test score, because the model starts correcting the remaining
noise too.

## The comparison — and a trap

Three models on the same data:

```
              test    CV mean    CV spread
baseline      0.700
tree (d=2)    0.960     0.827      0.049
forest        0.900     0.867      0.063
boosting      0.880     0.873      0.053
```

**Read the test column and the tree wins: 0.96.** It beats both the forest
and boosting. So what is all this ensemble business for?

**Nothing — if you believe that number.**

Remember section 05: on a test set of 50 records, one record moves the score
by 0.02. The 0.96 is the peak of the jumping we saw in the depth sweep; not
a real advantage but a lucky draw.

**Read the cross validation column:** tree 0.827, forest 0.867, boosting
0.873. The order reverses, and this time it is **the mean of five
measurements** speaking.

This is the module's most repeated lesson: **one number does not settle a
question about a model.**

## Feature importance is steadier

In section 07 we saw the tree give `age` an importance of 0.0 — at depth 2
its turn never came. The forest:

```
tree  : age 0.000   income 0.454   visits 0.546
forest: age 0.232   income 0.344   visits 0.424
```

**No column gets zero importance in the forest.** There are hundreds of
trees and each works with a different subset of features, so `age` gets
tried over and over. Its real contribution surfaces.

**This shows why a single tree saying "this column is useless" cannot be
trusted.** The forest's ranking is both steadier and fairer.

The same warnings still apply though: **importance is not causation**,
correlated columns still share importance, and high-cardinality columns
still inflate.

## Free validation: OOB

Bagging has a pleasant by-product. Each tree **never sees** roughly a third
of the training data (the rows that missed its bootstrap sample). Those rows
are a test set for that tree.

```python
model = RandomForestClassifier(n_estimators=200, oob_score=True,
                               random_state=42)
model.fit(X_train, y_train)
print(model.oob_score_)
```

```
trees   oob_score   test
   10       0.873   0.860
   50       0.880   0.880
  200       0.887   0.900
```

**OOB gives an estimate without setting aside a separate validation set**,
and it comes out fairly close to the test score. It is cross validation's
cheap alternative: computed from trees you already trained, with no extra
training.

It still does not replace the test set — OOB comes from the training data,
and the final measurement is still made on the untouched test set.

## What it costs

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">speed</span><span class="anat-body">200 trees = 200 times the training; predictions slow down too</span></div>
    <div class="anat-row"><span class="anat-label">readability</span><span class="anat-body"><b>lost</b> — you cannot turn 200 trees' rules into a sentence</span></div>
    <div class="anat-row"><span class="anat-label">memory</span><span class="anat-body">every tree is stored separately</span></div>
  </div>
  <figcaption>Section 07's greatest advantage goes here: a single tree's rules could be explained to a stakeholder; a forest's cannot.</figcaption>
</figure>

When interpretability really is needed there are two routes: present a
single shallow tree alongside as an **explanation**, or describe the forest
indirectly with tools like feature importance and partial dependence.

## Which one when

| Situation | Choice |
|---|---|
| A fast, sturdy starting point | **Random forest** |
| The highest accuracy and time to tune | **Gradient boosting** |
| You have to explain the rule to a person | **A single tree** |
| Little data and a linear relationship | **A linear model** |
| Predictions must be very fast | A single tree or a linear model |

**A random forest is a good default** because it works reasonably without
tuning: make `n_estimators` large enough and the rest usually takes care of
itself. Gradient boosting offers a higher ceiling but wants
`learning_rate`, `n_estimators` and the depth tuned together.

## What we skipped in this section

- **XGBoost, LightGBM, CatBoost.** Faster and stronger implementations of
  gradient boosting; the most used in competitions and in industry. They are
  separate libraries, so they are not here.
- **`HistGradientBoostingClassifier`.** sklearn's fast boosting class; far
  faster than `GradientBoosting` on large data and **it can work with
  missing values**.
- **Stacking.** Feeding several different models' predictions into another
  model as input.

The next section looks at an entirely different problem: what happens when
one class is 95% of the data?
