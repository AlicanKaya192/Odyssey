A short version of everything in the lesson. Come back here when you get stuck on a question.

## Discrete distributions

| Distribution | $P(X = k)$ | $E[X]$ | $\operatorname{Var}(X)$ | When |
|---|---|---|---|---|
| Bernoulli($p$) | $p^k (1 - p)^{1 - k}$, $k \in \{0, 1\}$ | $p$ | $p(1 - p)$ | a single yes–no |
| Binomial($n, p$) | $\binom{n}{k} p^k (1 - p)^{n - k}$ | $np$ | $np(1 - p)$ | successes in $n$ independent trials |
| Poisson($\lambda$) | $\dfrac{e^{-\lambda} \lambda^k}{k!}$ | $\lambda$ | $\lambda$ | event counts at a constant rate |

Large $n$, small $p$ and $np = \lambda$: binomial $\approx$ Poisson.

## Continuous distributions

| Distribution | Density | $E[X]$ | $\operatorname{Var}(X)$ |
|---|---|---|---|
| Uniform($a, b$) | $\frac{1}{b - a}$ | $\frac{a + b}{2}$ | $\frac{(b - a)^2}{12}$ |
| Exponential($\lambda$) | $\lambda e^{-\lambda x}$ | $\frac{1}{\lambda}$ | $\frac{1}{\lambda^2}$ |
| Normal($\mu, \sigma^2$) | $\frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x - \mu)^2}{2\sigma^2}}$ | $\mu$ | $\sigma^2$ |

Exponential: $P(X > t) = e^{-\lambda t}$, memoryless.

## The normal distribution

- $\mu \pm \sigma$: $68$ percent; $\mu \pm 2\sigma$: $95$ percent;
  $\mu \pm 3\sigma$: $99.7$ percent.
- $Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1)$.

| $z$ | $0.5$ | $1$ | $1.5$ | $1.96$ | $2$ | $3$ |
|---|---|---|---|---|---|---|
| $P(Z \leq z)$ | $0.691$ | $0.841$ | $0.933$ | $0.975$ | $0.977$ | $0.999$ |

Symmetry: $P(Z \leq -z) = 1 - P(Z \leq z)$.

## In machine learning

| Model | Distribution |
|---|---|
| logistic regression, binary classification | Bernoulli |
| softmax, multi-class | categorical |
| linear regression, MSE | normal error |
| count regression | Poisson |

## Practical tips

- For "how many" with a fixed number of trials use the binomial; without
  one, the Poisson.
- "How long is the wait" is exponential.
- Turn a normal question into $z$ first, then look at the table.
- For "at least one" use the complement again: $1 - P(X = 0)$.
