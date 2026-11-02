The two approaches are not rivals; they answer different questions. Looking
at the same data both ways is often the healthiest.

| | Frequentist | Bayesian |
|---|---|---|
| What does probability describe? | the frequency over many repeats | how much we believe something |
| Parameter | a fixed but unknown number | an unknown with a distribution |
| Main output | p-value, confidence interval | posterior, credible interval, P(B > A) |
| Past knowledge | in the design (power calculation) | directly in the prior |
| What it controls | the false alarm rate (α) | the decision's expected loss |
| Weak side | hard to explain the result to a team | the prior can be argued about |

## Sentences that often get mixed up

- "95% confidence interval: the true value is here with 95% probability." →
  This sentence is right for a **credible interval**, not a confidence
  interval.
- "p = 0.03, so the probability B is better is 97%." → Wrong. That is a
  P(B > A) sentence; p does not say it.
- "With the Bayesian method I can look and stop whenever I like." → Looking
  is free, but if the stopping rule is not written in advance, the frequency
  of wrong decisions still rises.

## When does the Bayesian view help?

- When the decision maker needs direct numbers like "the probability B is
  better" and "our loss if we are wrong".
- When there is reliable past data and the sample is small.
- When estimating many small groups together (e.g. hundreds of products),
  shrinkage prevents believing the extremes.
