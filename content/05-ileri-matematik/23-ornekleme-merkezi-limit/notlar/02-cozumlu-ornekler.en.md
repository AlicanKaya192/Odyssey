A worked example for each method in the lesson, step by step. Try each question yourself first, then read the solution.

## 1. Parameter or statistic?

**Question:** In a survey $42$ percent of $500$ people said "yes". What is
the nationwide "yes" rate, and what is $0.42$?

The nationwide rate $p$ is the unknown parameter; $\hat{p} = 0.42$ is the
statistic that estimates it.

## 2. Standard error

**Question:** $\sigma = 20$, $n = 100$. What is the standard error of the
sample mean?

$\frac{20}{10} = 2$.

## 3. The sample size needed

**Question:** If $\sigma = 15$, how many observations are needed for a
standard error of at most $1.5$?

$\frac{15}{\sqrt{n}} \leq 1.5$, $\sqrt{n} \geq 10$, $n \geq 100$.

## 4. A probability for the mean

**Question:** $\mu = 50$, $\sigma = 10$, $n = 25$. What is
$P(\bar{X} < 47)$?

$\text{SE} = 2$, $z = -1.5$: $1 - 0.933 = 0.067$.

## 5. An interval for the mean

**Question:** In the same setting, what is $P(48 \leq \bar{X} \leq 52)$?

$z = \pm 1$: about $0.682$.

## 6. The distribution of a total

**Question:** Package weights have $\mu = 500$ g and $\sigma = 20$ g. What
are the mean and standard deviation of the total weight of a box of $40$?

Mean $40 \cdot 500 = 20{,}000$ g. Standard deviation $20\sqrt{40} \approx
126.5$ g. The spread of the total grows, but shrinks relative to its mean.

## 7. The standard error of a proportion

**Question:** The true proportion is $0.3$ and $n = 100$. What is the
standard error of $\hat{p}$?

$\sqrt{\frac{0.3 \cdot 0.7}{100}} = \sqrt{0.0021} \approx 0.046$.

## 8. The uncertainty of test accuracy

**Question:** A model scored $85$ percent accuracy on $500$ test examples.
What is the standard error?

$\sqrt{\frac{0.85 \cdot 0.15}{500}} \approx 0.016$, that is about $\pm 1.6$
points.

## 9. A biased sample

**Question:** An app's satisfaction survey was sent only to people still
using the app; $10{,}000$ answers came back. Does the result represent all
users?

No: those who left are not in the sample. $10{,}000$ answers do not fix the
bias; they only make the biased estimate look more precise.

## 10. The bootstrap

**Question:** The sample is $\{2, 4, 9\}$. How is one bootstrap resample
drawn?

Draw three times at random, with replacement: for example $\{4, 4, 9\}$,
with mean $\approx 5.67$. Repeating this hundreds of times, the
distribution of the means estimates the sampling distribution.
