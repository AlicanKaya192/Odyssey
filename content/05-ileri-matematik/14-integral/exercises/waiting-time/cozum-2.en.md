**Idea:** Build $F(t) = P(X \le t)$ (the **cumulative distribution function**) once; every question is read off it.

**Step 1 — $F$.** $F(t) = \int_0^t 2e^{-2x} \, dx = \big[-e^{-2x}\big]_0^t = 1 - e^{-2t}$.

**Step 2 — Read it off.** Total: $\lim_{t \to \infty} F(t) = 1$. $P(X \le 1) = F(1) = 0.8647$.

**Step 3 — Invert.** $F(m) = \frac{1}{2}$: $m = \frac{\ln 2}{2}$.

**Why the same result?** The fundamental theorem: $F$ is an antiderivative of the density, and $F' = f$. Every probability is a difference of two values of $F$: $P(a \le X \le b) = F(b) - F(a)$. The `cdf` functions in statistics libraries are exactly this $F$.

**Answer:** $1$, $0.865$, $0.347$.
