The diagnosis starts by putting the two scores side by side. The treatment
depends on the diagnosis, and **a wrong diagnosis sends you the wrong way.**

## The diagnosis table

| Training | Test | Situation | Direction |
|---|---|---|---|
| Excellent | Poor | **Overfitting** | Simplify |
| Poor | Poor | **Underfitting** | Complicate |
| Good | Good | Nothing wrong | Leave it |
| Poor | Good | Something is off | Check the split and the code |

The last row is rare and almost always a sign of a mistake: the sets got
mixed, there is leakage, or the test set happens to be easy.

## Overfitting: seven fixes

**1. Simplify the model.**

There are hyperparameters that tune complexity directly:

| Model | Setting | Direction |
|---|---|---|
| Decision tree | `max_depth` | Lower it |
| Decision tree | `min_samples_leaf` | Raise it |
| KNN | `n_neighbors` | Raise it |
| Random forest | `max_depth`, `min_samples_leaf` | Constrain them |
| Linear model | `alpha` (Ridge/Lasso) | Raise it |

**2. Collect more data.**

The learning curve tells you whether this will help: it will if a gap
remains between the curves, it will not if they have met.

**3. Reduce the number of features.**

As the number of features approaches the number of samples, memorising gets
easier. Removing columns weakly related to the target can improve the model.

**But do the selection on the training side** — choosing by looking at all
the data is leakage.

**4. Use regularisation.**

Linear models have versions that penalise large coefficients:

```python
from sklearn.linear_model import Ridge, Lasso

model = Ridge(alpha=1.0)     # shrinks the coefficients
model = Lasso(alpha=0.1)     # drives some coefficients to zero
```

The larger `alpha` is, the simpler the model. **These models need scaling**,
because the penalty looks at the size of the coefficient.

**5. Move to ensemble methods.**

A random forest damps a single tree's memorisation by averaging many trees.
That is section 8.

**6. Stop early.**

For models that learn in rounds (gradient boosting, neural networks),
stopping when the validation score starts to worsen.

**7. Reduce the noise.**

Wrong labels and outliers give the model something to memorise. Cleaning the
data works as a treatment for overfitting too.

## Underfitting: four fixes

**1. Complicate the model.** Raise the depth, lower the neighbour count, try
a tree instead of a line.

**2. Add features.** You cannot expect a model to learn something it does
not know about. The residual plot tells you which column is missing
(section 2).

**3. Build derived features.** If the relationship is curved, putting `x**2`
next to `x` lets a linear model capture the curve. The product or ratio of
two columns can carry information too.

**4. Loosen the regularisation.** If `alpha` is too large the model may have
been simplified too far.

## Complexity against error

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">too simple</span><span class="anat-body">training and test error are <b>both high</b> — underfitting</span></div>
    <div class="anat-row"><span class="anat-label">balanced</span><span class="anat-body">the test error is at its <b>lowest</b></span></div>
    <div class="anat-row"><span class="anat-label">too complex</span><span class="anat-body">the training error falls to zero and <b>the test error rises again</b></span></div>
  </div>
  <figcaption>What you are looking for is the point where the test error is lowest, not where the training error is.</figcaption>
</figure>

**In practice that curve does not come out smooth.** On small test sets the
numbers jump, and picking the lowest point by eye means deciding on noise.
Cross validation exists for exactly that reason.

## Complex is not always better

Measured on this module's car data:

```
decision tree (depth 5)   MAE 64.33
decision tree (no limit)  MAE 66.21
linear regression         MAE 16.50
```

Linear regression is four times better than the decision tree. The reason is
the data: the price really is set by a linear relationship, and the tree is
trying to imitate it in steps.

**Choosing a model is not a matter of fashion but of measurement.** Measuring
the simple one before trying something "more advanced" usually saves time.

## A checklist

Before you start improving a model:

1. **Did you measure both scores?** The test score alone gives no
   diagnosis.
2. **Does it beat the baseline?** If not, complexity is not the issue.
3. **Did you cross validate?** A difference from a single split may be
   noise.
4. **Did you look at the spread?** If the gap between two means is smaller
   than the spread, it means nothing.
5. **What does the learning curve say?** Do you need data or a model?
6. **Is there a pattern in the residuals?** If there is, a feature is
   missing.

Changing a model before answering these six is turning knobs in the dark.
