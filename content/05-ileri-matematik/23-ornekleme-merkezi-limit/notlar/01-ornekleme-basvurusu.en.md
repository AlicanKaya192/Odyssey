A short version of everything in the lesson. Come back here when you get stuck on a question.

## Concepts

| Concept | Meaning |
|---|---|
| population | all the units of interest |
| sample | $n$ units chosen from the population |
| parameter | a number of the population ($\mu$, $\sigma$, $p$); unknown |
| statistic | computed from the sample ($\bar{x}$, $s$, $\hat{p}$) |
| sampling distribution | the distribution of a statistic from sample to sample |
| standard error | the standard deviation of a statistic |
| unbiased | $E[\text{estimate}] = \text{parameter}$ |

## Formulas

| What | Formula |
|---|---|
| expected value of the mean | $E[\bar{X}] = \mu$ |
| standard error of the mean | $\frac{\sigma}{\sqrt{n}}$ ($\frac{s}{\sqrt{n}}$ if $\sigma$ is unknown) |
| standard error of a proportion | $\sqrt{\frac{p(1 - p)}{n}}$ |
| standard deviation of a sum | $\sigma\sqrt{n}$ |
| standardising | $Z = \dfrac{\bar{X} - \mu}{\sigma / \sqrt{n}}$ |

## The Central Limit Theorem

For large $n$ (roughly $n \geq 30$), $\bar{X} \approx \mathcal{N}\!\left(\mu,
\frac{\sigma^2}{n}\right)$; the shape of the population does not matter. The
observations must be independent.

## Practical tips

- Is the question about one observation or a mean? For a mean, divide the
  standard deviation by $\sqrt{n}$.
- To cut the error $k$ times, you need $k^2$ times the data.
- Size does not help a biased sample; look at how it was chosen first.
- If a total is asked, its mean is $n\mu$ and its standard deviation
  $\sigma\sqrt{n}$.
