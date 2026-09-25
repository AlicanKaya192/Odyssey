A short version of everything in the lesson. Come back here when you get stuck on a question.

## Discrete and continuous

| | Discrete | Continuous |
|---|---|---|
| distribution | $p(x) = P(X = x)$ | density $f(x)$ |
| total | $\sum p(x) = 1$ | $\int f(x) \, dx = 1$ |
| probability | $P(X = a) = p(a)$ | $P(a \leq X \leq b) = \int_a^b f$; $P(X = a) = 0$ |
| $E[X]$ | $\sum x \, p(x)$ | $\int x \, f(x) \, dx$ |
| $E[g(X)]$ | $\sum g(x) \, p(x)$ | $\int g(x) \, f(x) \, dx$ |

Cumulative distribution $F(x) = P(X \leq x)$.

## Rules

| Rule | Formula |
|---|---|
| linearity | $E[aX + b] = aE[X] + b$ |
| sum | $E[X + Y] = E[X] + E[Y]$ (always) |
| variance | $\operatorname{Var}(X) = E[(X - \mu)^2] = E[X^2] - \mu^2$ |
| shift and scale | $\operatorname{Var}(aX + b) = a^2 \operatorname{Var}(X)$ |
| independent sum | $\operatorname{Var}(X \pm Y) = \operatorname{Var}(X) + \operatorname{Var}(Y)$ |
| mean | $E[\bar{X}] = \mu$, $\operatorname{Var}(\bar{X}) = \frac{\sigma^2}{n}$ |

## Ready-made values

| Variable | $E[X]$ | $\operatorname{Var}(X)$ |
|---|---|---|
| a die | $3.5$ | $\frac{35}{12}$ |
| uniform $[0, 1]$ | $\frac{1}{2}$ | $\frac{1}{12}$ |
| uniform $[a, b]$ | $\frac{a + b}{2}$ | $\frac{(b - a)^2}{12}$ |

## In machine learning

- The training loss estimates the expected loss with a sample mean.
- A mini-batch gradient is unbiased; its variance falls as the batch grows.
- Dropout: scale a kept neuron by $\frac{1}{p}$ and the expected output is
  preserved.

## Practical tips

- First check that the distribution adds up to $1$.
- For the variance, compute $E[X^2]$ separately, then subtract $\mu^2$.
- Remember that a factor enters the variance squared.
- A density value is not a probability; probability is area.
