**Idea:** $\text{loss} = -\ln p$ ($y = 1$). $\frac{\partial\,\text{loss}}{\partial w} = \frac{d\,\text{loss}}{dp} \cdot \frac{dp}{dz} \cdot \frac{\partial z}{\partial w}$.

**Step 1 — $p$.** $z = 0.5$, $p \approx 0.622$.

**Step 2 — The links.** $\frac{d\,\text{loss}}{dp} = -\frac{1}{p} \approx -1.607$; $\frac{dp}{dz} = p(1 - p) \approx 0.235$; $\frac{\partial z}{\partial w} = x = 2$. The product is $\approx -1.607 \cdot 0.235 \cdot 2 \approx -0.755$.

**Step 3 — Update.** $0.5 + 0.0755 = 0.5755$.

**Why the same result?** $-\frac{1}{p} \cdot p(1 - p) = -(1 - p) = p - 1 = p - y$; the $p$ in the sigmoid's derivative cancels the $\frac{1}{p}$ in the logarithm's. The short formula is the result of this cancellation.

**Answer:** $0.622$, $-0.755$ and $0.5755$.
