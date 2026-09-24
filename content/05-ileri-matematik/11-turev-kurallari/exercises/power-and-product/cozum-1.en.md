**What is asked?** The value at a point of the derivative of a function made of powers, and of a product.

**Idea:** Writing the root and the fraction as powers puts every term under the power rule. For the product, the product rule.

**Step 1 — $f'$.** $f(x) = x^3 - 4x^{1/2} + 2x^{-1}$:

$$
f'(x) = 3x^2 - 2x^{-1/2} - 2x^{-2} = 3x^2 - \frac{2}{\sqrt{x}} - \frac{2}{x^2}
$$

**Step 2 — $f'(4)$.** $48 - \frac{2}{2} - \frac{2}{16} = 48 - 1 - 0.125 = 46.875 = \frac{375}{8}$.

**Step 3 — $h'$.** $h'(x) = 2x(x - 3) + (x^2 + 1)$; $h'(2) = 4 \cdot (-1) + 5 = 1$.

**Check:** A central difference for $h$, with step $0.01$: $h(2.01) = 5.0401 \cdot (-0.99) = -4.989699$, $h(1.99) = 4.9601 \cdot (-1.01) = -5.009701$; the difference over $0.02$ is $1.0001$ ✓.

**Watch out:** In the derivative of $-4\sqrt{x}$ the coefficient is $-4 \cdot \frac{1}{2} = -2$; in the derivative of $\frac{2}{x}$ the sign becomes minus.

**Answer:** $f'(4) = \frac{375}{8} = 46.875$, $h'(2) = 1$.
