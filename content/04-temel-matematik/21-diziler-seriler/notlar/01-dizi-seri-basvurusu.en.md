A short version of everything in the lesson. Come back here when you get stuck on a question.

## Two sequences

| | Arithmetic | Geometric |
|---|---|---|
| step | add $d$ | multiply by $r$ |
| general term | $a_1 + (n - 1)d$ | $a_1 r^{n-1}$ |
| $d$ or $r$ | next minus previous | next over previous |
| sum of the first $n$ terms | $\dfrac{n(a_1 + a_n)}{2}$ | $a_1 \dfrac{1 - r^n}{1 - r}$ |
| relative | a line | an exponential function |

From two terms: there are $m - k$ steps between $a_m$ and $a_k$.
Arithmetic: $d = \dfrac{a_m - a_k}{m - k}$; geometric:
$r^{m - k} = \dfrac{a_m}{a_k}$.

## Sigma notation

$\displaystyle \sum_{i=a}^{b} t_i$: the counter goes from $a$ to $b$; the
number of terms is $b - a + 1$.

| Rule | Written as |
|---|---|
| sum | $\sum (a_i + b_i) = \sum a_i + \sum b_i$ |
| constant factor | $\sum c \, a_i = c \sum a_i$ |
| constant term | $\sum_{i=1}^{n} c = nc$ |
| product (no such rule) | $\sum a_i b_i \neq \sum a_i \cdot \sum b_i$ |

## Ready-made sums

| Sum | Result |
|---|---|
| $\sum_{i=1}^{n} i$ | $\dfrac{n(n + 1)}{2}$ |
| $\sum_{i=1}^{n} i^2$ | $\dfrac{n(n + 1)(2n + 1)}{6}$ |
| $\sum_{k=0}^{n-1} r^k$ | $\dfrac{1 - r^n}{1 - r}$ |
| $\sum_{k=0}^{\infty} r^k$, $-1 < r < 1$ | $\dfrac{1}{1 - r}$ |

## In machine learning

| What | Formula |
|---|---|
| mean | $\frac{1}{n} \sum x_i$ |
| MSE | $\frac{1}{n} \sum (y_i - \hat{y}_i)^2$ |
| weighted sum | $\sum w_i x_i + b$ |
| discounted reward | $\sum \gamma^t r_t$ |

## Practical tips

- The $n$th term is reached in $n - 1$ steps.
- Find the number of terms: $\frac{\text{last} - \text{first}}{d} + 1$.
- If a Σ is unclear, write out its first three terms.
- Before using the infinite sum formula, check that $r$ is between $-1$
  and $1$.
