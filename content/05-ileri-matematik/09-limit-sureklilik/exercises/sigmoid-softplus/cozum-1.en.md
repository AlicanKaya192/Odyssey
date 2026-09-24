**What is asked?** How two activations behave at infinity.

**Idea:** The key in all of them is $e^{-x}$: it goes to zero as $x \to \infty$ and grows without bound as $x \to -\infty$. The third has an $\infty - \infty$ indeterminacy; the logarithms must be combined into one term.

**Step 1 — The sigmoid, plus infinity.** $e^{-x} \to 0$: $\sigma(x) \to \frac{1}{1 + 0} = 1$.

**Step 2 — The sigmoid, minus infinity.** $e^{-x} \to \infty$: the bottom grows without bound, so $\sigma(x) \to 0$.

**Step 3 — Softplus minus $x$.**

$$
\begin{aligned}
\ln(1 + e^x) - x &= \ln(1 + e^x) - \ln e^x \\
&= \ln \frac{1 + e^x}{e^x} = \ln\left(e^{-x} + 1\right)
\end{aligned}
$$

As $x \to \infty$, $e^{-x} + 1 \to 1$ and $\ln 1 = 0$.

**Check:** $x = 10$: $e^{-10} \approx 0.000045$; $\ln(1.000045) \approx 0.000045$. Very close to zero ✓.

**Watch out:** Finishing $\ln(1 + e^x) - x$ directly with "$\infty - \infty = 0$" reaches the right answer by a wrong road; the same reasoning would say $\ln(1 + e^x) - x/2$ goes to $0$ too, yet it grows without bound. An indeterminate form is not decided before it is rewritten.

**Answer:** $1$, $0$ and $0$.
