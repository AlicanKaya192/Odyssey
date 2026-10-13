In this module we saw every step of a text classification project. When you
start a new project, go through this list in order.

## Data

- [ ] **Look** at the texts: read 50 random examples. Are there encoding
  problems, HTML leftovers, invisible spaces (01)?
- [ ] Count the class distribution. If it is imbalanced, the measure is
  macro F1, not accuracy (09).
- [ ] Find exact and near duplicates (13). If the same text is in both
  training and test, the score is inflated.
- [ ] Who gave the labels, and how? Label a few examples yourself and
  compare: how much label noise is there?

## Measuring

- [ ] Split off the test data **at the very start** and do not touch it
  until the end. With `stratify`.
- [ ] Measure the baseline: the most common class, a simple rule (00, 15).
- [ ] Which error is more expensive for the business? Precision or recall
  (09)?

## Model

- [ ] Put preprocessing inside the Pipeline (10): cleaning, masking (15).
- [ ] Start with simple, strong baselines: TF-IDF + logistic regression,
  linear SVM, Naive Bayes (08, 09).
- [ ] Word pairs catch negation (09); character n-grams help on text with
  many typos (10).
- [ ] Search settings with cross-validation; `best_score_` is optimistic
  (10).

## Inspection

- [ ] Look at the confusion matrix and the per-class F1 (09).
- [ ] Read the most confident mistakes (09): is the model wrong, or the
  label?
- [ ] Do the errors come from the limits of the task (two-topic tickets,
  irony)? Then the fix is the task's definition, not the model (11, 15).
- [ ] Consider an "I am not sure" gate for out-of-scope input (the first
  note of this section).

## Use

- [ ] Save the Pipeline to a single file; keep your own functions in a
  module (10).
- [ ] In real use incoming texts change over time. Label new examples now
  and then and measure the model again.

This list holds in the next module too. There we will represent text not
with word counts but with **embeddings**; yet the steps of measuring,
splitting and inspecting stay exactly the same.
