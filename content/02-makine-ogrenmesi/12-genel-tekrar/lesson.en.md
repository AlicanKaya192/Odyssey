# Overall Review

Twelve sections ago we started with "what is machine learning". You can now
build a model end to end, measure it honestly and save it.

This section teaches nothing new. **It collects what you learned into a
single flow** and shows the most confused parts once more, with measured
numbers.

## The flow

Every problem goes through the same six steps:

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>read,<br><code>X</code> and <code>y</code></span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>split and close<br>the test set</span>
    <span class="arrow">&rarr;</span>
    <span class="node acc"><b>3</b><br>measure the<br>baseline</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>4</b><br>pipeline +<br>cross validation</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>5</b><br>measure once<br>on test</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>6</b><br>save and<br>write the note</span>
  </div>
  <figcaption>Any report that skips step three is incomplete; any report that does step five twice is wrong.</figcaption>
</figure>

## The baseline comes before everything

This module's most repeated sentence. Three measured examples:

| Problem | Baseline | Model | Gap |
|---|---|---|---|
| Car price (MAE) | 137.3 | **16.2** | 8× lower error |
| Subscriber churn | 0.573 | **0.793** | 22 points |
| Fraud | 0.944 | 0.955 | **1.1 points** |

The third row is why this table exists. **95.5% accuracy means nothing**,
because a predictor that does nothing scores 94.4%. The models in the first
two rows really work; the third one only reveals itself under recall.

## Choosing a model is a measurement task

The answer to "which model is best?" depends on the data and is **not known
in advance.** Two measured examples that contradict each other:

**Car price (regression):**

| Model | Cross-validation MAE | Test MAE |
|---|---|---|
| **Linear regression** | **16.6 ± 2.8** | **16.2** |
| Random forest | 42.3 ± 15.1 | 44.2 |
| Decision tree | 69.3 ± 10.2 | 65.7 |

The simplest model beats the most complex one fourfold. The reason was
measured in section 07: when the relationship really is linear, trees try to
imitate it with steps and lose. An ensemble does not rescue that — the
problem is not the number of trees but that a tree does not suit the data.

**Customer churn (classification, section 08):**

| Model | Test on one split | Cross validation |
|---|---|---|
| Decision tree | **0.96** | 0.827 |
| Random forest | 0.90 | 0.867 |
| Gradient boosting | 0.88 | **0.873** |

Here the order **reverses with the measurement.** A single test score puts
the tree first; the mean of five folds puts it last.

**The one rule from both:** you do not choose the model, the measurement
does. And that measurement **cannot be a single number.**

## Choosing the metric comes before choosing the model

Section 09's lesson reaches across the whole module. The same model, the
same data, four different numbers:

```
accuracy           0.955    <- baseline 0.944, so almost nothing
precision          0.750
recall             0.286    <- 15 of 21 frauds escaped
average precision  0.525    <- baseline 0.056, so nine times the baseline
```

**Choosing which one to report changes more than choosing the model.**

A rough guide:

| Situation | What to read |
|---|---|
| Regression | MAE and R², with the baseline beside them |
| Balanced classification | Accuracy + the confusion matrix |
| Imbalanced classification | Recall, F1, **average precision** |
| Misses are expensive | Recall first |
| False alarms are expensive | Precision first |
| Clustering | The silhouette — **with its noise reference** |

## Leakage: the module's most expensive mistake

It appeared in three separate sections in three different forms, and in all
three it **raised the score.** The sign of leakage is not a bad result but
one that is **too good.**

| Where | What happens | Measured effect |
|---|---|---|
| Section 04 | The scaler is fitted before the split | A "working" model on random data |
| Section 11 | Feature selection outside cross validation | 0.716 → **0.780** |
| This section | A column recorded after the outcome | 0.815 → **1.000** |

The last one meets you in the third exercise. A model gives **100%
accuracy** and its confusion matrix holds not one error. That is not a
success but an alarm.

**The defences, in order:**

1. `train_test_split` — close the test set at the very start.
2. **A pipeline** — tie the preprocessing to the model so each fold does its
   own preparation in cross validation.
3. **Think column by column:** will this information really be in my hands
   at the moment I make the prediction? The `followup_calls` column is
   written **after** the patient is discharged.

No tool can do the third. That one is yours.

## Overfitting and instability

| Symptom | Diagnosis | Remedy |
|---|---|---|
| Training 1.000, test 0.80 | Overfitting (high variance) | Simplify, add data, **bagging** |
| Training 0.70, test 0.70 | Underfitting (high bias) | A stronger model, **boosting** |
| Different results on the same data | Instability | A forest; measured: 14 points → 8 |
| A very wide CV spread | Too little data or too few positives | Not more folds, more data |

**Training at 1.000 in a forest is not overfitting.** Measured in section
08: with 25 trees, training 1.000 and test 0.90; with 300 trees, 0.90
again. Because each tree memorises different things, the average stays
clean.

That is the **exact opposite** of the same table for a single tree, which is
why the two get confused.

## Scaling: where it is needed

| Model | Scaling | Measured |
|---|---|---|
| KNN | **Mandatory** | 0.64 → 0.92 |
| K-means | **Mandatory** | 0.202 → 0.517 |
| PCA | **Mandatory** | It works on variance |
| Logistic regression | Useful | It speeds up convergence |
| Decision tree | **Pointless** | 0.80 → 0.80 |
| Random forest | **Pointless** | Everything inside is a tree |

The rule in one sentence: **anything that computes a distance or a variance
wants scaling; anything that looks at ordering wants none.**

## What a pipeline solves

Section 11's gain is not shorter code:

- **Leakage becomes structurally impossible.** `cross_val_score` retrains
  every step inside each fold.
- **The model is saved complete.** The medians, the mode, the encoder's
  categories, the scaling values and the coefficients, all in one file.
- **Predictions can be made from raw data** — even raw data with missing
  values.

Measured: for a row with empty `city` and `monthly` the model returns 0.466.
With a hand-prepared model that row would have been a crash.

## What you can do

- Take a table, identify the target, set a baseline and decide whether a
  model really works
- Tell regression and classification apart and pick the right metric for
  each
- Prepare dirty data (missing values, text columns, scale differences)
  without leaking
- Diagnose overfitting and measure honestly with cross validation
- Recognise five model families: linear, KNN, tree, ensemble, clustering
- See through accuracy's lie on imbalanced data and choose a threshold
  deliberately
- Look for groups in unlabelled data and **question whether what you found
  is real**
- Tie all of it into a single object and save it

## What you cannot do

To be honest, this list is longer:

- **Deep learning.** Images, audio and text stayed outside this module.
  Neural networks are a field of their own and start with `torch`.
- **Time series.** On sequential data `train_test_split` is **wrong** — you
  end up seeing the future. Time-based splitting and `TimeSeriesSplit` are
  needed.
- **Text and embeddings.** Turning a sentence into numbers is its own
  subject (`TfidfVectorizer` to start, embeddings after).
- **Causality.** Nowhere in this module did we say "this column causes
  that". A model finds correlation; finding causes is experiment design.
- **Shipping to production.** Serving, monitoring, versioning — MLOps.
- **Collecting data.** The most expensive and most skipped part. Here the
  data arrived ready; in real life it does not.

## A closing word

One habit ran through this whole module: **do not guess, measure.**

Whether the tree or the forest wins, whether scaling is needed, what `k`
should be, where to put the threshold — we knew none of it. We measured all
of it, and in some cases intuition was wrong.

The quiz below covers all twelve sections, and the exercises are five
end-to-end projects. In the third one you will be handed a model that works
**perfectly.** You are expected to be suspicious.
