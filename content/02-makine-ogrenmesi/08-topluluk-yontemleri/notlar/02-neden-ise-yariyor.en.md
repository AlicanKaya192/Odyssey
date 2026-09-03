"Many weak models together become strong" sounds like magic. It is not;
there is a single idea behind it.

## Two kinds of error

A model's error splits in two:

| Kind | What it means | Example |
|---|---|---|
| **Bias** | The model is wrong systematically | Drawing a straight line through a curved relationship |
| **Variance** | A small change in the data changes the result a lot | A deep tree's root threshold moving |

You saw both in section 05: underfitting is high bias, overfitting is high
variance.

**Ensemble methods attack the two by two different routes.**

## Bagging reduces variance

A single tree's error is largely random: this row dropped so the threshold
moved, that row entered so a branch changed.

Averaged, random errors **cancel out.** Like tossing the same coin a hundred
times and averaging: one toss is unpredictable, the average of a hundred is
very close to 0.5.

The measured result:

```
tree scores  : [0.92, 0.88, 0.78, 0.80, 0.80, 0.84]  -> a 14-point range
forest scores: [0.90, 0.84, 0.86, 0.90, 0.90, 0.92]  -> an 8-point range
```

**Bagging does not touch bias.** If every tree makes the same systematic
mistake, so does their average. This is why bagged models are kept **deep**:
their bias is already low, and what needs reducing is variance.

## Independence is essential

For averaging to help, the errors have to be **independent of one another**.
If every tree makes the same mistake, the average corrects nothing.

A random forest's second randomness (`max_features`) exists precisely for
this: at each split a subset of features is hidden so the trees take
different routes.

This produces a counterintuitive result: **weakening each tree individually
strengthens the ensemble.** The trees' individual accuracy falls, but their
dependence on one another falls further.

## Boosting reduces bias

Boosting's logic is entirely different. The trees are shallow and weak — one
alone knows almost nothing.

But they are built in sequence and each new tree looks at **the remaining
error**:

```
prediction = tree1 + lr * tree2 + lr * tree3 + ...
```

At each step the error shrinks a little further. So the ensemble builds,
**step by step**, a complexity no single model could reach.

**This is why boosting can overfit:** take enough steps and the remaining
"error" is nothing but noise, which the model then tries to correct too. A
forest has no such danger, because there the trees do not correct one
another.

## Why trees

The ensemble idea works with any model, but it works especially well with
trees:

- **Trees are unstable.** The diversity to average is already there.
  Averaging a hundred linear regressions gives almost the same line — there
  is nothing to average.
- **Trees need no preparation.** No scaling, no encoding order, no outlier
  trouble.
- **Trees are fast.** Building hundreds is feasible.

## When it does not help

| Situation | Why |
|---|---|
| Very little data | The bootstrap samples come out nearly identical |
| The relationship really is linear | A linear model is already best; trees struggle with steps |
| One feature decides everything | The trees cannot diversify |
| Interpretability is essential | An ensemble loses readability entirely |

It was measured in section 05: on the car data the tree's error was 64 and
linear regression's 16.5. An ensemble does not rescue that — the problem is
not the number of trees but that a tree does not suit the data.

## A rough summary

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Is the model too unstable?</h4>
      <p>Different results on the same data, a large training-test gap.<br><b>Bagging / forest</b></p>
    </div>
    <div class="versus-side">
      <h4>Is the model too simple?</h4>
      <p>Poor on both training and test, cannot catch the pattern.<br><b>Boosting</b></p>
    </div>
  </div>
  <figcaption>The diagnosis comes from section 05's two-score table; the treatment is what changes here.</figcaption>
</figure>

In practice both are tried and compared **with cross validation** — because
there is no way to know in advance which error the data leans towards.
