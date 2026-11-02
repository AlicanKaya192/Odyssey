## "Revenue was not significant, so revenue did not rise."

A small test cannot see an effect in a noisy metric. The right sentence:
"In this test the revenue difference could not be measured." If revenue
matters, a bigger test or variance reduction is needed.

## "Buying rose by 10%."

Written alone, the relative change makes a small difference look big. The
base rate and the point difference are written together: "from 11.7% to
13.0%, +1.2 points."

## "The difference is bigger on mobile, let's ship it for mobile."

Picking a segment after looking at the result is a multiple comparison. If
the segment analysis was not planned before the test, it is only an idea
for a new experiment (the Segments and Simpson's Paradox section).

## "p = 0.001, so the effect is huge."

p does not tell the size of the effect (Effect Size section). The size is
in the interval.

## "The interval contains zero but p = 0.06, almost significant."

The threshold was chosen before the test. Changing the decision with
"almost" is choosing the threshold afterwards.

## "Let's run the test one more week, maybe it becomes significant."

Extending the duration after looking at the result inflates the false
alarm rate; we will measure this in The Peeking Trap and Sequential Testing
section.
