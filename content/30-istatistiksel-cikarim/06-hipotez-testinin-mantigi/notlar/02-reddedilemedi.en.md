The most often misread result of a test is "$H_0$ was not rejected". Most
people read it as "no difference". It is not.

## Absence of evidence is not evidence of absence

In this section's server test there was a real 40 ms slowdown and the test
did not show it (p = 0.0968). The simulation said this 40-measurement
design catches the real slowdown only 52.5% of the time. The test
did not say "no slowdown"; it said "I cannot tell with this much data".

## What to write?

- Not "no difference" but: "The difference was not statistically
  significant."
- Put the confidence interval of the difference next to it. If the interval
  is wide and contains both zero and an important slowdown, the result is
  **inconclusive**: more data is needed.
- Only if the interval is narrow and contains only trivial values ("at most
  5 ms") can you say "practically no difference".

## With low power a test says nothing

A test with 20% power misses four out of five real differences. Its "not
significant" tells you almost nothing. That is why computing **before** the
experiment how many measurements are needed (power analysis) matters as much
as the test itself.

## Two wrong reactions

- "Not significant, so the change is harmless, let us ship it." A missed
  slowdown still reaches users.
- "Let us measure a bit more until it becomes significant." Adding data
  after looking at the result inflates the false alarm rate (in the second
  module: the peeking trap). The number of measurements is fixed in advance.
