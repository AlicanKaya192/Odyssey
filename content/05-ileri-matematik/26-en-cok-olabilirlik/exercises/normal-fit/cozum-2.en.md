**Idea:** $\ell = -\frac{n}{2}\ln(2\pi v) - \frac{1}{2v}\sum(x_i - \mu)^2$ with $v = \sigma^2$. Set both partial derivatives to zero.

**Step 1 — $\mu$.** $\frac{\partial\ell}{\partial\mu} = \frac{1}{v}\sum(x_i - \mu) = 0$; $\sum x_i = 5\mu$, $\hat{\mu} = 12$.

**Step 2 — $v$.**

$$
\frac{\partial\ell}{\partial v} = -\frac{n}{2v} + \frac{S}{2v^2} = 0
$$

Here $S = \sum(x_i - \hat{\mu})^2 = 26$; the solution is $v = \frac{S}{n} = 5.2$.

**Step 3 — Unbiased.** $\frac{S}{n - 1} = 6.5$; the MLE does not make this correction.

**Why the same result?** The ready formulas are exactly the solution of these two equations; the $n$ in the $v$ equation comes straight from the likelihood, while $n - 1$ comes from a separate wish for unbiasedness.

**Answer:** $12$, $5.2$ and $6.5$.
