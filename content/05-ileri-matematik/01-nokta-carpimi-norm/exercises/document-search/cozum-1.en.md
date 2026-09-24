**What is asked?** Which document is more like the query? We measure similarity not by the size of the word counts but by their **direction**: two vectors pointing the same way talk about the same topic.

**Idea:** Cosine similarity is the cosine of the angle between two vectors:

$$
\cos(\mathbf{q}, D) = \frac{\mathbf{q} \cdot D}{\|\mathbf{q}\|\,\|D\|}
$$

Dividing the dot product by the lengths takes the document's length out of the calculation. The closer the result is to $1$, the more alike the directions.

**Step 1 — The dot products.** Multiply matching components and add:

$$
\begin{aligned}
\mathbf{q} \cdot D_1 &= 1 \cdot 2 + 1 \cdot 2 + 0 \cdot 1 = 4 \\
\mathbf{q} \cdot D_2 &= 1 \cdot 0 + 1 \cdot 6 + 0 \cdot 8 = 6
\end{aligned}
$$

**Step 2 — The lengths.**

$$
\begin{aligned}
\|\mathbf{q}\| &= \sqrt{1 + 1 + 0} = \sqrt{2} \\
\|D_1\| &= \sqrt{4 + 4 + 1} = \sqrt{9} = 3 \\
\|D_2\| &= \sqrt{0 + 36 + 64} = \sqrt{100} = 10
\end{aligned}
$$

**Step 3 — The cosines.** $\sqrt{2} \approx 1.414$:

$$
\begin{aligned}
\cos(\mathbf{q}, D_1) &= \frac{4}{\sqrt{2} \cdot 3} \approx \frac{4}{4.243} \approx 0.94 \\
\cos(\mathbf{q}, D_2) &= \frac{6}{\sqrt{2} \cdot 10} \approx \frac{6}{14.14} \approx 0.42
\end{aligned}
$$

**Reading the result:** Looking at the plain dot product, $D_2$ ($6 > 4$) would seem more similar. But $D_2$ is mostly about *probability*; its numbers are large only because it is a long document. Once the cosine divides the length away, $D_1$, which is about the same topic as the query (*vector* and *matrix*), wins clearly.

**Watch out:** Forget to divide by the lengths and long documents come first in every search.

**Answer:** $0.94$ and $0.42$; $D_1$ is more similar.
