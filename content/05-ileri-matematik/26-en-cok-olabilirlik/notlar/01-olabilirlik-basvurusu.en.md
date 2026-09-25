A short version of everything in the lesson. Come back here when you get stuck on a question.

## Definitions

| Concept | Formula |
|---|---|
| likelihood | $L(\theta) = \prod_{i} f(x_i \mid \theta)$ (data fixed) |
| log-likelihood | $\ell(\theta) = \sum_{i} \ln f(x_i \mid \theta)$ |
| MLE | $\hat{\theta} = \arg\max_\theta \ell(\theta)$ |
| negative log-likelihood | $\text{NLL} = -\ell(\theta)$, minimised |
| Laplace correction | $\hat{p} = \frac{k + 1}{n + 2}$ |

## Ready results

| Distribution | MLE |
|---|---|
| Bernoulli / binomial | $\hat{p} = \frac{k}{n}$ |
| Poisson | $\hat{\lambda} = \bar{x}$ |
| Exponential | $\hat{\lambda} = \frac{1}{\bar{x}}$ |
| Normal | $\hat{\mu} = \bar{x}$, $\hat{\sigma}^2 = \frac{1}{n}\sum (x_i - \bar{x})^2$ |
| Categorical | $\hat{p}_k = \frac{n_k}{n}$ |

## Steps

1. Write $\ell(\theta) = \sum \ln f(x_i \mid \theta)$; drop the constants.
2. Solve $\ell'(\theta) = 0$.
3. Check that the second derivative is negative (or check the endpoints).
4. Without a closed-form solution, apply gradient descent to the NLL.

## The link to losses

| Model assumption | NLL |
|---|---|
| normal noise, fixed $\sigma$ | sum of squared errors (MSE) |
| Bernoulli target | log-loss (binary cross-entropy) |
| categorical target | cross-entropy |

## Practical tips

- Take logs: the product becomes a sum and small numbers do not underflow.
- $g(\hat{\theta})$ is the MLE of $g(\theta)$ (invariance).
- Do not give $0$ to an outcome never seen; add a correction or a prior.
