**Idea:** Without memorising the formula: at each step replace $L$ by its quadratic Taylor approximation at that point and find the bottom of that parabola.

**Step 1 — The parabola at $w = 0$.** $L(0) = 1$, $L'(0) = -1$, $L''(0) = 1$: $q(\Delta) = 1 - \Delta + \frac{\Delta^2}{2}$. $q'(\Delta) = -1 + \Delta = 0$: $\Delta = 1$, new $w = 1$.

**Step 2 — The parabola at $w = 1$.** $L'(1) = e - 2$, $L''(1) = e$: $q'(\Delta) = (e - 2) + e\Delta = 0$, $\Delta = -\frac{e - 2}{e} \approx -0.264$. New $w \approx 0.736$.

**Step 3 — The true bottom.** $L'(w) = 0$: $w = \ln 2 \approx 0.693$.

**Why the same result?** The bottom of $q(\Delta) = L + L'\Delta + \frac{1}{2}L''\Delta^2$ is at $\Delta = -\frac{L'}{L''}$; the Newton formula is this calculation itself. The step is as accurate as the parabola is close to the real curve; at the second step the parabola is built nearer the bottom, so the approximation is much better.

**Answer:** $1$, $0.736$, $0.693$.
