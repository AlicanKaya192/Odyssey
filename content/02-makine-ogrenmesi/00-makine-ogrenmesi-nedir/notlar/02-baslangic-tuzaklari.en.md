None of the mistakes in this note are code mistakes. The code runs, the
model is built, a number comes out — and the number misleads.

## 1. Testing the model on the data it was trained on

The most basic mistake. A model can memorise its training data; being 99%
correct on it says nothing.

```python
model.fit(X, y)
model.score(X, y)     # meaningless
```

The right way: split the data and measure on the **test** set. That number
is an exam mark, and the questions must not be handed out in advance.

## 2. Celebrating a score without a baseline

"80% correct" is not information on its own. If 80 of a hundred records
belong to one class, a single line that predicts that class for everything
is also 80% correct.

| Problem | Baseline |
|---|---|
| Regression | Predict the mean of the training data |
| Classification | Predict the most frequent class |

If the model cannot beat it, there is no model.

## 3. Looking at accuracy on imbalanced data

If ten of a thousand patients are ill, a model that says "nobody is" is
**99% correct**. And useless: it finds none of the ten people it was
supposed to find.

On imbalanced data accuracy is a silencing number; you look at precision,
recall and the confusion matrix. That is sections 3 and 9.

## 4. Confusing regression with classification

A numeric target means regression, a categorical one classification. The
distinction decides the method **and the measure**: MAE is meaningless for
classification, accuracy for regression.

The line is sometimes blurred ("how many stars"). You make the call — and
you **write down the call you made**.

## 5. Forgetting to scale

If one column runs 0 to 1 and another 0 to 100,000, methods based on
distance (like KNN) hear only the large column. The small one behaves as
though it were not there.

Tree methods are unaffected; KNN, linear models and clustering are. That is
sections 4 and 6.

## 6. Data leakage

The model seeing, during training, information it will **not have** at
prediction time.

The classic example: scaling the whole dataset and splitting afterwards. The
test set's mean leaks into training and the test score comes out higher than
it should.

The second classic: predicting an illness using an "admission date" column.
The model works beautifully, because a column already tells it the answer.

The rule: **split first, then touch.** Sections 4 and 11.

## 7. Choosing settings by looking at the test set

Looking at the test set and saying "that setting was better" turns the test
into training data. Try twenty settings and pick the best by test score, and
that score is no longer honest.

The right way: choose settings on a **validation** set or with cross
validation, and look at the test set once, at the end. That is section 5.

## 8. Building a complex model on little data

Growing a deep tree on thirty rows does nothing but memorise them. On little
data a simple model does more work.

A rough habit: when the number of features approaches the number of samples,
the model is almost certainly memorising.

## 9. Believing the model tells you causes

If a model says "price rises with floor area", that is an **association**.
The rule from the previous module holds here too; a model does not change
it.

Feature importances are the same: "the most important variable" does not
mean that variable is the **cause**.

## 10. Not fixing the randomness

Splitting data and many models involve randomness. Without `random_state`
every run gives a different result, and you cannot tell improvement from
luck.

If you want to compare results, fix the randomness.

## 11. Expecting a good model from dirty data

Missing values, inconsistently written categories and outliers go into the
model as they are. That is what the whole previous module was for, and it is
still half the work here.

## 12. Reducing the result to a single number

"The model's R² is 0.85" is not a report. On what data, with how many
records, against which baseline, and where does it go wrong — that is the
report.

**Where** a model is wrong matters as much as how often it is right.
