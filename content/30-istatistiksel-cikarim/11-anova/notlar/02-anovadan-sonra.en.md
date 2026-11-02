ANOVA saying "significant" is not the end of the road but the start. On its
own it only says "the groups are not all the same". Three more questions
need answers before a decision.

## 1. Which groups differ?

Use a post-hoc test such as Tukey HSD. Testing six pairs with uncorrected
t-tests multiplies false alarms, just as it did before ANOVA.

If only a few **pre-planned** comparisons interest you (for example
comparing each new layout only with the old layout A), you do not need to
look at all pairs; there are more powerful methods for those few
comparisons (in the second module: multiple comparisons).

## 2. How big is the difference?

In this section F was large and p tiny, but $\eta^2$ = 0.037: only a
small part of the time comes from the layout. Layout C differs from A by
about 1.4 minutes; whether that matters for the business is decided by the
page's purpose.

## 3. Does the result carry over to real life?

- Were the groups randomly assigned? If not (if users chose the layout
  themselves), the difference may come from the people who chose rather
  than from the layout.
- Was the measurement period long enough? A new layout may attract
  curiosity in the first days and then lose its effect (the novelty effect,
  in the second module).

## If ANOVA says "not significant"

It does not mean all layouts are the same. With small groups real
differences are easily missed. In this section even Tukey could not tell
apart the real 0.6 minutes between C and D with 150 people each. In the
power analysis section we will learn to compute in advance how many people
are enough.
