**Idea:** For large $x$, the dominant part of $1 + e^x$ is $e^x$. Take it out as a factor: $1 + e^x = e^x(1 + e^{-x})$. The same move works for the sigmoid: multiply top and bottom by $e^x$.

**Step 1 — Rewrite the sigmoid.** $\sigma(x) = \dfrac{e^x}{e^x + 1}$. As $x \to -\infty$, $e^x \to 0$: $\frac{0}{0 + 1} = 0$. As $x \to \infty$, divide top and bottom by $e^x$: $\frac{1}{1 + e^{-x}} \to 1$.

**Step 2 — Softplus.** $\ln\big(e^x(1 + e^{-x})\big) = x + \ln(1 + e^{-x})$, by the product rule of logarithms.

**Step 3 — Take the difference.** $s(x) - x = \ln(1 + e^{-x}) \to \ln 1 = 0$.

**Why the same result?** $\ln \frac{1 + e^x}{e^x}$ and $\ln(1 + e^{-x})$ are the same expression; the first comes from the quotient rule, the second from the product rule. Both are the single move that removes the indeterminacy: taking out the dominant term. The result also shows why softplus behaves like ReLU for large inputs: $s(x) \approx x$.

**Answer:** $1$, $0$, $0$.
