**Idea:** The centred vector is the sum of the part along the component and the part perpendicular to it: $\lVert x - \bar{x}\rVert^2 = z_1^2 + \lVert\text{error}\rVert^2$.

**Step 1 — Score.** $z_1 = 2\sqrt{2}$, $z_1^2 = 8$.

**Step 2 — Reconstruction.** $\bar{x} + z_1u_1$; the first coordinate is $2 + 2\sqrt{2} \cdot \frac{1}{\sqrt{2}} = 4$.

**Step 3 — Error.** $\lVert(3, 1)\rVert^2 = 10$; the error is $10 - 8 = 2$.

**Why the same result?** Reconstruction is an orthogonal projection, so the error vector is perpendicular to the projection; Pythagoras holds for the sum of two perpendicular vectors. The equivalence of PCA's "maximise variance" and "minimise error" views comes from this equality too.

**Answer:** $2.828$, $4$ and $2$.
