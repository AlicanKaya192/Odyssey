**What is asked?** The fit of a regression line.

**Idea:** SSE is the model's error, SST the error of a model using no features; $R^2$ is the gain between them.

**Step 1 — SSE.** Residuals $3 - 3.6 = -0.6$, $7 - 5.2 = 1.8$, $5 - 6.8 = -1.8$, $9 - 8.4 = 0.6$. Squares $0.36 + 3.24 + 3.24 + 0.36 = 7.2$.

**Step 2 — SST.** $\bar{y} = 6$; deviations $-3, 1, -1, 3$; sum of squares $20$.

**Step 3 — $R^2$.** $1 - \frac{7.2}{20} = 0.64$.

**Check:** The residuals sum to $0$ ✓; $\sum x e = -1.2 + 7.2 - 10.8 + 4.8 = 0$ ✓ (perpendicularity).

**Watch out:** Taking $R^2$ as $\frac{\text{SSE}}{\text{SST}}$ gives the unexplained share; $R^2$ is its complement to $1$.

**Answer:** $7.2$, $20$, $0.64$.
