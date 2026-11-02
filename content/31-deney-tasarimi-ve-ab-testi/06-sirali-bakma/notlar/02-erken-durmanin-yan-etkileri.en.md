Even with the right thresholds, stopping early has two side effects.

## The effect is exaggerated

Tests that stop early stop at moments when the effect looks large by
chance. The **winner's curse** from the Power Analysis section applies here
too: the effect measured in tests that stop early is larger than the true
effect on average. This is taken into account when the effect is
reported; if possible, the effect is re-estimated with data collected after
stopping.

## The weekly cycle breaks

If a two-week test stops on day 4, only weekday users may have been seen.
In an audience that behaves differently at weekends, the result does not
represent the whole week. That is why sequential designs usually place the
looks at **the ends of full weeks**.

## The novelty effect

In the first days users may click on something new out of curiosity; this
effect fades later. A test that stops too early can mistake this temporary
rise for a lasting one (Novelty Effects and Long-Term Impact section).

## Summary

Stopping early, even when done right, means "deciding with less
information". It is chosen when speed is truly valuable (e.g. a large harm
or a very valuable win); otherwise a fixed-duration test is cleaner.
