The way to judge an estimation rule is to run it on thousands of samples
and look at its behaviour. In this section we did that three times.

## 1. Unbiasedness: is it right on average?

If the average of the estimates over thousands of samples equals the truth,
the estimator is unbiased.

- The sample mean: unbiased.
- The variance dividing by $n-1$: unbiased; dividing by $n$: underestimates.
- The sample maximum: biased; 99.9% of samples stayed below the
  truth.

## 2. Consistency: does it approach the truth as it grows?

If the estimates gather around the truth as the sample grows, the estimator
is consistent. The wobble of the sample mean shrinks with $\sqrt{n}$; in the
first section we saw 400-person samples gather much more tightly than
25-person ones.

A biased estimator can still be consistent: the bias of the variance
dividing by $n$ disappears as the sample grows.

## 3. Efficiency: how little does it wobble with the same data?

Of two unbiased estimators, the one that wobbles less is more efficient. For
bell-shaped load times the median's variance was about 1.53 times
the mean's: the median needs more data for the same precision.

## A combined measure: mean squared error

Sometimes a slightly biased estimator that wobbles very little is better
than an unbiased one that wobbles a lot. The number that measures both
together is the **mean squared error**:

$$MSE = \text{bias}^2 + \text{variance}$$

Regularisation in machine learning makes exactly this trade: it accepts a
little bias to reduce the wobble.

## Checklist

- Judge an estimator by simulation, not by a single number.
- Test it on data whose truth you know (like our population).
- Write the bias, the wobble and their sum separately.
