**Idea:** With one feature $R^2 = r^2$; also $\text{SSE} = (1 - r^2)\,\text{SST}$.

**Step 1 — Sums.** The $x$ deviations are $-3, -1, 1, 3$; the $y$ deviations $-3, 1, -1, 3$. $S_{xy} = 9 - 1 - 1 + 9 = 16$, $S_{xx} = 20$, $S_{yy} = 20$.

**Step 2 — SST and $r$.** $\text{SST} = S_{yy} = 20$. $r = \frac{16}{\sqrt{20 \cdot 20}} = 0.8$.

**Step 3 — $R^2$ and SSE.** $R^2 = 0.64$; $\text{SSE} = 0.36 \cdot 20 = 7.2$.

**Why the same result?** $\text{SSE} = S_{yy} - \frac{S_{xy}^2}{S_{xx}}$ (after substituting the least squares solution); and $\frac{S_{xy}^2}{S_{xx}S_{yy}}$ is exactly $r^2$.

**Answer:** $7.2$, $20$ and $0.64$.
