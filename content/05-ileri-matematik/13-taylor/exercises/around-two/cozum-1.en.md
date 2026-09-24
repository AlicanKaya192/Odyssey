**What is asked?** A coefficient and a value of the Taylor polynomial at a point other than zero.

**Idea:** $P_2(x) = f(2) + f'(2)(x - 2) + \frac{f''(2)}{2}(x - 2)^2$.

**Step 1 — The derivatives.** $f(2) = \frac{1}{2}$, $f'(2) = -\frac{1}{4}$, $f''(2) = \frac{2}{8} = \frac{1}{4}$.

**Step 2 — The polynomial.** $P_2(x) = \frac{1}{2} - \frac{1}{4}(x - 2) + \frac{1}{8}(x - 2)^2$. The coefficient is $\frac{1}{8}$.

**Step 3 — The value.** $x - 2 = 0.2$: $0.5 - 0.05 + 0.005 = 0.455$.

**Check:** $\frac{1}{2.2} = 0.4545\ldots$; the difference is $0.0005$. The term left out is $-\frac{1}{16} \cdot 0.2^3 = -0.0005$ ✓.

**Watch out:** Taking $f''(2) = \frac{1}{4}$ as the coefficient; the coefficient is $\frac{f''(2)}{2!} = \frac{1}{8}$.

**Answer:** $\frac{1}{8}$ and $0.455$.
