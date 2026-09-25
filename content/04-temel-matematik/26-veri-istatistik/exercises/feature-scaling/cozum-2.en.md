**Idea:** Both scalings are lines: $z = \frac{x - 30}{10\sqrt{2}}$ and $x' = \frac{x - 10}{40}$. Putting the value into the line's equation is enough.

**Step 1 — The standard deviation.** The values are symmetric around $30$ in steps of $10$; $\sigma^2 = \frac{2 \cdot 400 + 2 \cdot 100}{5} = 200$, $\sigma = 10\sqrt{2}$.

**Step 2 — $z(45)$.** $\frac{15}{10\sqrt{2}} = \frac{3}{2\sqrt{2}} = \frac{3\sqrt{2}}{4} \approx 1.061$.

**Step 3 — $x'(60)$.** The slope is $\frac{1}{40}$; from $10$ to $60$ is $50$ units: $\frac{50}{40} = 1.25$.

**Why the same result?** Scaling is a linear function made of a shift and a division; whatever value goes in is transformed by the same rule. Because the rule's coefficients are fixed on the training data, a test value can land outside the range.

**Answer:** $14.142$, $1.061$ and $1.25$.
