**Idea:** Instead of the product rule, expand the product and differentiate it as a polynomial; for $f$, work out each term separately with the derivatives from the table.

**Step 1 — $f'(4)$, term by term.** $(x^3)' = 3x^2 \to 48$. $(\sqrt{x})' = \frac{1}{2\sqrt{x}} \to \frac{1}{4}$, times $-4$: $-1$. $(\frac{1}{x})' = -\frac{1}{x^2} \to -\frac{1}{16}$, times $2$: $-\frac{1}{8}$. Total $48 - 1 - \frac{1}{8} = \frac{375}{8}$.

**Step 2 — Expand $h$.** $(x^2 + 1)(x - 3) = x^3 - 3x^2 + x - 3$.

**Step 3 — The derivative.** $h'(x) = 3x^2 - 6x + 1$; $h'(2) = 12 - 12 + 1 = 1$.

**Why the same result?** The product rule gives $2x(x - 3) + x^2 + 1 = 2x^2 - 6x + x^2 + 1 = 3x^2 - 6x + 1$; exactly the polynomial obtained by expanding and differentiating. The product rule is really needed for products that are hard to expand (such as $x^2 e^x$); here both ways are short.

**Answer:** $\frac{375}{8}$ and $1$.
