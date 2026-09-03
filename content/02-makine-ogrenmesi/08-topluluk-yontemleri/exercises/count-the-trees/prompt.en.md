How many trees should a forest have? In sections 05 and 07, raising the
depth started to hurt past a point. Is it the same here?

**What you need to do:**

1. Prepare and split the data.
2. Try these tree counts: **1, 5, 25, 100, 300**.
3. Measure the training and test accuracy for each and print one line:
   **the count, training, test**.
4. Print `same` if 25 trees and 300 trees give the same test score,
   `different` otherwise.

**Expected output:**

```
1 0.947 0.72
5 0.993 0.84
25 1.0 0.9
100 1.0 0.9
300 1.0 0.9
same
```

**One tree gives 0.72, twenty-five give 0.90.** Adding trees helps — up to a
point. After 25 nothing changes.

**Now look at what really matters: the training column sits at 1.000 while
the test column DOES NOT FALL.**

This is the opposite of everything you saw in section 05. There, as the
depth grew, training climbed to 1.000 and test fell — overfitting. Here
training is at 1.000 and test does not fall.

**The reason:** because each tree sees the data differently, they memorise
different things. Since their memorisations do not overlap, the average
stays clean. A hundred trees have no shared mistake.

**The conclusion:** `n_estimators` is not a balance parameter but a **cost**
parameter. Raising it does not damage the model, only slow it down.
Somewhere between 100 and 300 is a common start; more is usually wasted
time.

**A warning:** this is true only for a **forest**. In gradient boosting,
raising the tree count can cause overfitting, because there the trees
correct one another and eventually start correcting the noise too.
