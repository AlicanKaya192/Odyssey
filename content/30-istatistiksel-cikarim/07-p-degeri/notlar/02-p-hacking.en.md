**p-hacking** means examining the same data in different ways and reporting
whatever comes out with p < 0.05. Usually there is no bad intent: each step
looks reasonable on its own. But every new try adds a new chance of a false
alarm; in this section, looking at 20 metrics made the chance that at least
one is "significant" 62.6%.

## Common forms

| What is done | Why it misleads |
|---|---|
| Looking at many metrics and highlighting the significant one | Each metric is a separate try |
| Splitting the data into segments ("significant on mobile only") | Each segment is a separate try |
| Collecting data until it becomes significant | Each interim look is a separate try |
| Dropping or keeping outliers depending on the result | The analysis is chosen from the data |
| Switching to a one-sided test after seeing the result | The false alarm rate doubles |
| Trying different tests and picking the smallest p | Each test is a separate try |

## Safeguards

- **Write it down first:** the question, the primary metric, the sample
  size, the test, the direction and $\alpha$ are documented before the data
  arrives (pre-registration).
- **One primary metric:** other metrics are reported separately and
  cautiously as "exploration".
- **Multiple comparison correction:** if many things really are tested, the
  threshold is tightened accordingly (Bonferroni, Holm; in the second
  module).
- **Report everything:** say how many things were examined, including the
  ones that were not significant.

## The question to ask yourself

"If the data had come out differently, would I have done the analysis the
same way?" If the answer is "no", the p-value does not keep its promise.
