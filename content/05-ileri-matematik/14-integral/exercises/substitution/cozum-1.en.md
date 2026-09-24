**What is asked?** Two definite integrals with nested functions.

**Idea:** If a function and its derivative sit together inside, $u$ is that function. In a definite integral the limits are converted to $u$ as well.

**Step 1 — The first.** $u = x^2 + 1$, $du = 2x \, dx$; $x = 0 \to u = 1$, $x = 1 \to u = 2$:

$$
\int_1^2 u^3 \, du = \left[\frac{u^4}{4}\right]_1^2 = \frac{16 - 1}{4} = \frac{15}{4}
$$

**Step 2 — The second.** $u = 2x$, $du = 2 \, dx$; the limits are $0$ and $2 \ln 2$:

$$
\frac{1}{2} \int_0^{2 \ln 2} e^u \, du = \frac{1}{2}\left(e^{2 \ln 2} - 1\right) = \frac{1}{2}(4 - 1) = \frac{3}{2}
$$

**Check:** $e^{2 \ln 2} = (e^{\ln 2})^2 = 2^2 = 4$ ✓.

**Watch out:** Switching to $u$ but keeping the limits $0$ and $1$ gives $\frac{1}{4}$ in the first; the limits change together with the variable.

**Answer:** $\frac{15}{4}$ and $\frac{3}{2}$.
