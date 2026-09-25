**What is asked?** How the correlation of the errors decides the benefit of averaging.

**Idea:** $\operatorname{Var}\!\left(\frac{e_1 + e_2}{2}\right) = \frac{\sigma^2(1 + \rho)}{2}$.

**Step 1 — $\rho = 0.6$.** $\frac{9 \cdot 1.6}{2} = 7.2$.

**Step 2 — $\rho = 0.2$.** $\frac{9 \cdot 1.2}{2} = 5.4$.

**Step 3 — Target $6$.** $\frac{9(1 + \rho)}{2} = 6$, $1 + \rho = \frac{4}{3}$, $\rho = \frac{1}{3} \approx 0.333$.

**Check:** At $\rho = 1$ it is $9$ (no benefit), at $\rho = 0$ it is $4.5$ (halved); the values found lie between these ✓.

**Watch out:** Scaling the average by $\frac{1}{2}$ scales the variance by $\frac{1}{4}$; multiplying by $\frac{1}{2}$ is wrong.

**Answer:** $7.2$, $5.4$, $\approx 0.333$.
