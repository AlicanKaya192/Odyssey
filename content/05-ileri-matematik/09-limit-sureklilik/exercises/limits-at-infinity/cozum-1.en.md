**What is asked?** The values two fractions go to as $x$ grows without bound.

**Idea:** Substituting gives an indeterminate form like $\frac{\infty}{\infty}$. Dividing every term on top and bottom by $x^2$ sends the small terms to zero and leaves numbers.

**Step 1 — The first limit.**

$$
\frac{4x^2 - 3x}{2x^2 + 5} = \frac{4 - \frac{3}{x}}{2 + \frac{5}{x^2}} \;\to\; \frac{4 - 0}{2 + 0} = 2
$$

**Step 2 — The second limit.**

$$
\frac{5x + 1}{x^2 + 2} = \frac{\frac{5}{x} + \frac{1}{x^2}}{1 + \frac{2}{x^2}} \;\to\; \frac{0}{1} = 0
$$

**Check:** The degree rule: in the first the degrees are equal, and the leading coefficients give $\frac{4}{2} = 2$ ✓. In the second the bottom's degree is larger, so the limit is $0$ ✓.

**Watch out:** Divide by the **highest** power on top and bottom, not by the top's; in the second limit, dividing by $x$ leaves an $x$ in the bottom and the indeterminacy remains.

**Answer:** $2$ and $0$.
