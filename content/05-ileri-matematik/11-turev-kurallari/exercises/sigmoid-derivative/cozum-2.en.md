**Idea:** Without relying on the form $\sigma(1 - \sigma)$, substitute directly into the formula from the chain rule, $\sigma'(x) = \dfrac{e^{-x}}{(1 + e^{-x})^2}$.

**Step 1 — $x = 0$.** $e^0 = 1$: $\frac{1}{(1 + 1)^2} = \frac{1}{4}$.

**Step 2 — $x = \ln 3$.** $e^{-x} = \frac{1}{3}$:

$$
\frac{1/3}{(4/3)^2} = \frac{1}{3} \cdot \frac{9}{16} = \frac{3}{16}
$$

**Step 3 — Four layers.** $\frac{1}{4^4} = \frac{1}{256}$.

**Why the same result?** $\frac{e^{-x}}{(1 + e^{-x})^2}$ and $\sigma(1 - \sigma)$ are two ways of writing the same expression; the algebra in the lesson showed this. In practice the second form wins: $\sigma$ has already been computed in the forward pass, so the derivative is a single multiplication.

**Answer:** $\frac{1}{4}$, $\frac{3}{16}$, $\frac{1}{256}$.
