**Idea:** Take the $\ln$ of both sides: powers and exponents turn into factors. Then use $(\ln y)' = \frac{y'}{y}$.

**Step 1 — For $y$.** $\ln \lvert y \rvert = 4 \ln \lvert 2x^2 - 3 \rvert$. Differentiating: $\frac{y'}{y} = \frac{4 \cdot 4x}{2x^2 - 3}$.

**Step 2 — $x = 1$.** $y(1) = (-1)^4 = 1$, $\frac{y'}{y} = \frac{16}{-1} = -16$; $y'(1) = -16 \cdot 1 = -16$.

**Step 3 — For $z$.** $\ln z = -\frac{x^2}{2}$, whose derivative gives $\frac{z'}{z} = -x$. $z'(1) = -1 \cdot e^{-1/2} \approx -0.607$.

**Why the same result?** The rule $(\ln y)' = \frac{y'}{y}$ is itself the chain rule ($\ln$ outer, $y$ inner). The logarithm brings the power down in front and shortens the chain; for expressions with many factors this road takes far fewer steps.

**Answer:** $-16$ and $-0.607$.
