**Idea:** First bring the vectors to unit length; the dot product of unit vectors is directly the cosine.

**Step 1 — Dot product.** $24$.

**Step 2 — Unit vectors.** $\hat{a} = \frac{a}{5} = (0.8, \ 0, \ 0.6)$; $\lVert b \rVert = \sqrt{26} \approx 5.099$, $\hat{b} \approx (0.588, \ 0.196, \ 0.784)$.

**Step 3 — Cosine.** $\hat{a} \cdot \hat{b} \approx 0.8 \cdot 0.588 + 0.6 \cdot 0.784 \approx 0.471 + 0.471 = 0.941$.

**Why the same result?** $\frac{a}{\lVert a \rVert} \cdot \frac{b}{\lVert b \rVert} = \frac{a \cdot b}{\lVert a \rVert\lVert b \rVert}$; dividing before or after is the same. In similarity search the vectors are normalised once and stored, then only dot products are taken.

**Answer:** $24$, $5.099$ and $0.941$.
