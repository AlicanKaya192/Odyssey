**1. Dot products:**

$$
\begin{aligned}
\mathbf{q} \cdot D_1 &= 2 + 2 + 0 = 4 \\
\mathbf{q} \cdot D_2 &= 0 + 6 + 0 = 6
\end{aligned}
$$

**2. Lengths:**

$$
\begin{aligned}
\|\mathbf{q}\| &= \sqrt{2} \\
\|D_1\| &= \sqrt{4 + 4 + 1} = 3 \\
\|D_2\| &= \sqrt{0 + 36 + 64} = 10
\end{aligned}
$$

**3. Cosines:**

$$
\cos(\mathbf{q}, D_1) = \frac{4}{3\sqrt{2}} \approx 0.94
$$

$$
\cos(\mathbf{q}, D_2) = \frac{6}{10\sqrt{2}} \approx 0.42
$$

**What happened?** Going by the plain dot product, $D_2$ ($6 > 4$) would look more similar. Yet $D_2$ is mostly about *probability*; its numbers are large only because it is long. Once the cosine divides the length away, $D_1$, which is about the same topic as the query, is clearly ahead.

**Answer: $0.94$ and $0.42$; $D_1$ is more similar**
