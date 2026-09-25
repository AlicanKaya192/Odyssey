**What is asked?** A point's projection onto one component, its reconstruction, and the part lost.

**Idea:** $z_1 = u_1^\mathsf{T}(x - \bar{x})$, $\hat{x} = \bar{x} + z_1u_1$.

**Step 1 — Score.** $x - \bar{x} = (3, 1)$; $z_1 = \frac{3 + 1}{\sqrt{2}} = 2\sqrt{2} \approx 2.828$.

**Step 2 — Reconstruction.** $z_1u_1 = 2\sqrt{2} \cdot \frac{1}{\sqrt{2}}(1, 1) = (2, 2)$; $\hat{x} = (4, 5)$.

**Step 3 — Error.** $x - \hat{x} = (1, -1)$; squared $2$.

**Check:** The error vector $(1, -1)$ is perpendicular to $u_1$: $(1, -1) \cdot (1, 1) = 0$ ✓.

**Watch out:** Taking $u_1^\mathsf{T}x = \frac{9}{\sqrt{2}}$ without subtracting the mean gives the wrong score; forgetting to add the mean back makes $\hat{x}$ $(2, 2)$.

**Answer:** $\approx 2.828$, $4$, $2$.
