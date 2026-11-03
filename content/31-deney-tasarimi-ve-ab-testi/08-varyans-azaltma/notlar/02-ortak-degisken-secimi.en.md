The gain from CUPED depends entirely on the choice of the covariate (X).

## A good X

- **Was measured before assignment.** The test cannot affect it, so its
  mean is the same in both groups and it does not shift the effect
  estimate.
- **Is strongly related to the metric.** Usually the best one is the same
  metric's value before the experiment: minutes before the test, purchases
  before the test.
- **Exists for everyone**, or if not, how it will be filled is written in
  advance.

## Users with no earlier data

Users who arrive for the first time during the test have no "earlier
minutes". The common solution is to fill X with the mean for them: then
X − X̄ is zero and these users stay unadjusted. This is valid but the gain
shrinks; if the share of new users is large, the benefit of CUPED drops
too.

## A bad X

- Anything measured during the test: sessions, clicks, add-to-carts. B can
  change these and the adjustment erases part of the effect.
- A "segment" computed after assignment (e.g. those very active during the
  test).
- An X chosen by looking at the result: trying one after another to pick
  the one with the biggest gain is another form of the trap from the
  Multiple Comparisons section. X is written into the plan in advance.
