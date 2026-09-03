# KNN

In section 00 you found the nearest neighbour by hand in an exercise. That
exercise had a name: **KNN**, K-Nearest Neighbours.

In this section you will use it on real data — and see how differently this
model works from the others.

## The model that does not learn

sklearn's three steps are the same here: build, `fit`, `predict`. But what
happens inside `fit` is entirely different.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Other models</h4>
      <p><code>fit</code> takes time; a rule is derived.<br><code>predict</code> is fast: apply the formula.</p>
    </div>
    <div class="versus-side">
      <h4>KNN</h4>
      <p><code>fit</code> finishes instantly: the data is <b>stored</b>.<br><code>predict</code> is expensive: a distance to every row.</p>
    </div>
  </div>
  <figcaption>This is why KNN is called a "lazy" model. The cost moves from training to prediction time.</figcaption>
</figure>

After training, linear regression kept two numbers (`coef_`, `intercept_`)
and forgot the data. KNN learns nothing: it **stores the whole training
set** and consults it on every prediction.

The practical consequence: as the training data grows, KNN's **prediction**
slows down. On a million rows, each prediction means a million distance
computations.

## How a prediction is made

Three steps:

1. Compute the distance from the new point to **every training row**.
2. Take the nearest **k** of them.
3. For classification, a **majority vote**; for regression, the **mean**.

The distance is usually Euclidean: the square root of the sum of the squared
differences.

On a small example with eight points, the nearest ones to a new point line
up like this:

```
distances: [0.71, 1.0, 2.92, 3.61, 4.03, 4.24, 4.3, 4.61]

k=1  ['A']                     -> A
k=3  ['A', 'B', 'B']           -> B
k=5  ['A', 'B', 'B', 'A', 'B'] -> B
```

**The answer changes with `k`.** `k=1` says A, `k=3` says B. The same data,
the same point, a different result. So `k` is not a small detail; it is the
model.

## Scaling is compulsory here

In section 04 we saw that scaling affects some models and not others. KNN is
at the head of the affected list, and the effect is larger than you might
expect.

The customer data has three columns: `age` (18-70), `income`
(12,000-200,000) and `visits` (1-50).

```
baseline (most frequent class)   0.70
KNN, unscaled                    0.64
KNN, scaled                      0.92
```

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Unscaled</h4>
      <p>Accuracy <b>0.64</b><br><b>Below</b> the baseline — a line that learns nothing does better.</p>
    </div>
    <div class="versus-side">
      <h4>Scaled</h4>
      <p>Accuracy <b>0.92</b><br>Beats the baseline decisively.</p>
    </div>
  </div>
  <figcaption>The same model, the same data, the same k. The only difference is bringing the columns onto a common scale.</figcaption>
</figure>

**Why so severe:** in a distance computation the gap between two customers
in `income` can be 100,000; in `visits` it is at most 49. In the sum of
squares the second does not even show up.

Unscaled, KNN is really **only looking at income.** The other two columns
were handed to the model and go unused.

**This means forgetting to scale can push the model below the baseline** —
a result worse than not building a model at all.

```python
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

`fit` on training, `transform` on both. Section 04's rule holds here too.

## What `k` tunes

`k` is a **hyperparameter**: the model does not learn it, you choose it. And
it tunes complexity directly.

```
 k   training   test
 1      1.000   0.820
 3      0.940   0.860
 5      0.940   0.920
 9      0.927   0.900
15      0.920   0.880
25      0.927   0.920
```

**At `k=1` the training accuracy is 1.000.** No surprise: every training
point's own nearest neighbour is itself. The model knows the training data
perfectly and drops to 0.820 on test — a textbook example of section 05's
overfitting table.

As `k` grows the training accuracy falls and the test accuracy first rises.
Too large a `k` blurs the boundaries: if `k` equalled the number of records,
the model would say the most frequent class for everything — it would become
the baseline.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">small k</span><span class="anat-body">sensitive to noise; a single odd neighbour flips the decision</span></div>
    <div class="anat-row"><span class="anat-label">large k</span><span class="anat-body">boundaries blur; small groups disappear</span></div>
    <div class="anat-row"><span class="anat-label">k = n</span><span class="anat-body">the model becomes the baseline: the most frequent class for everything</span></div>
  </div>
  <figcaption>Choosing an odd number is a common habit: in binary classification the votes cannot tie.</figcaption>
</figure>

## How to choose `k` — and a trap

Section 05's rule: a hyperparameter is chosen **with cross validation**, not
by looking at the test set.

The cross validation results on the training side:

```
 k   CV mean   CV std
 1     0.913    0.040
 3     0.893    0.039
 5     0.900    0.052
 7     0.873    0.057
 9     0.880    0.062
15     0.893    0.053
25     0.880    0.054
```

The highest mean is at `k=1`: 0.913. The choice looks settled.

**But look at the spread: 0.040.** The gap between best and worst is 0.040
(0.913 - 0.873) and the spread is 0.040 too. So **every value of k sits
inside the others' noise.** Cross validation cannot separate them here.

What do you do then? Section 05's sentence: "the difference has to exceed
the spread." When it does not, the choice is made on another ground — and
for KNN that ground is clear: **a larger `k` is more robust**, because it
does not hang on a single neighbour.

Let us see what happens on the test set:

```
CV winner            k=1   ->  test 0.820
largest k in noise   k=25  ->  test 0.920
```

**The naive choice costs ten points.** `k=1` was ahead in cross validation
by a hair, and that hair was noise.

This does not mean cross validation failed. Quite the opposite: because it
gave us the spread as well, we could say "this difference is meaningless".
Looking at the mean alone we would have picked `k=1` and been wrong.

## The decision boundary

The best way to see what `k` does is the **boundary** the model draws.

In a two-feature model (`income` and `visits`), producing a prediction for
every point of the plane and colouring it in gives us this:

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>k = 1</h4>
      <p>The boundary is <b>fragmented</b>: little islands around individual points. The model took every odd record seriously.</p>
    </div>
    <div class="versus-side">
      <h4>k = 15</h4>
      <p>The boundary is <b>smooth</b>: a single curve. Odd records dissolve into the majority.</p>
    </div>
  </div>
  <figcaption>Both have a test accuracy of 0.90. The same number, two entirely different models — a number alone does not describe a model.</figcaption>
</figure>

**This is visual proof of why one measure is not enough.** Two models give
the same accuracy, but one memorised the noise and the other caught the
general trend. On new data they will behave very differently.

## The curse of dimensionality

KNN's most serious limit: **as the number of features grows, distance loses
its meaning.**

It is counterintuitive, but in a high-dimensional space points end up almost
**equally** far from one another. The difference between the nearest and the
furthest neighbour melts away and the word "nearest" stops meaning anything.

The practical consequence: on data with fifty columns KNN is usually weak. A
method that works beautifully with three or five features collapses at
thirty.

The fixes: reduce the number of features, apply dimension reduction
(section 10), or move to a model that does not suffer from this — trees, for
instance.

## It works for regression too

The same idea holds for a numeric target: the **mean** of the nearest `k`
neighbours' target values.

```python
from sklearn.neighbors import KNeighborsRegressor
model = KNeighborsRegressor(n_neighbors=5)
```

You saw this in section 04: on the car data, unscaled KNN gave 171.49 and
scaled 51.48.

## Weighted voting

By default the five neighbours' votes count equally. You can also reduce a
distant neighbour's vote:

```python
KNeighborsClassifier(n_neighbors=5, weights="distance")
```

It sounds sensible, but it is **not automatically better.** On this data:

```
weights="uniform"    0.92
weights="distance"   0.88
```

Worse. The reason: distance weighting gives a very close neighbour
overwhelming power and the model drifts towards `k=1` — that is, towards
memorising.

Like every setting, this one is chosen **by trying**.

## When KNN is a good choice

| Good | Bad |
|---|---|
| Few features (2 to 10) | Many features (the curse of dimensionality) |
| Complex, curved boundaries | Very large data (slow predictions) |
| Small and medium datasets | Missing values (no distance can be computed) |
| You need a quick baseline | Interpretability matters |

**It has an interesting side on interpretability:** KNN cannot say why it
decided as it did (no coefficients, no rules) but it can show you **which
neighbours it looked at**. "I said this customer will leave because four of
the five most similar customers did" is a sentence you can make — and in
some settings that is more convincing than a coefficient.

## What we skipped in this section

- **Other distance measures.** Euclidean is the default;
  `metric="manhattan"` or cosine similarity for text data are also used.
- **Speeding it up.** With the `algorithm` parameter sklearn can use KD-trees
  and ball-trees, cutting prediction time on large data.
- **Missing values.** Because KNN computes distances it cannot work with
  gaps; they have to be filled first (section 04).

The next section takes an entirely different approach: models based not on
distance but on **questions** — decision trees.
