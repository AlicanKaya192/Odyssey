When the test ends and the change is opened to everyone, the question is
considered closed. But there are things a short test cannot see: the
novelty fading, the season, users changing their behaviour over time. A
**holdout** is set up for these.

## How it is set up

- When the change is opened, a small share of the users (e.g. 1–5%) is
  kept on the old version.
- This group is chosen at random, just as in the test; the salted hash
  method from the Random Assignment section is used here too.
- Months later the holdout is compared with everyone else: that is the
  lasting effect.

## Its cost

- Users in the holdout do not see the product thought to be better. The
  share is kept small.
- A small group is noisy; reading the result needs enough time.
- If many changes are opened one after another, the holdout measures their
  **combined** effect; the effects cannot be separated one by one.

## When is it needed?

- When the effect is expected to change over months (habit, novelty).
- When the decision involves a lot of money and the short test's estimate
  is the basis of the investment.
- When the metric reacts late (e.g. subscription cancellations, returning
  users).

## Remember

A holdout does not replace the test. The short test catches a harmful
change first; the holdout only corrects the size of the lasting effect.
