**Idea:** We can do the division in the cosine formula up front. If every vector is first turned into a unit vector (length 1), cosine similarity becomes a plain dot product, because the lengths in the denominator become $1 \cdot 1 = 1$. Search systems often work exactly like this.

**Step 1 — Find the lengths.** As in the first method: $\|\mathbf{q}\| = \sqrt{2}$, $\|D_1\| = 3$, $\|D_2\| = 10$.

**Step 2 — The unit vectors.** Divide every component by the vector's length ($1/\sqrt{2} \approx 0.707$):

$$
\begin{aligned}
\hat{\mathbf{q}} &= \frac{(1,\ 1,\ 0)}{\sqrt{2}} \approx (0.707,\ 0.707,\ 0) \\
\hat{D}_1 &= \frac{(2,\ 2,\ 1)}{3} \approx (0.667,\ 0.667,\ 0.333) \\
\hat{D}_2 &= \frac{(0,\ 6,\ 8)}{10} = (0,\ 0.6,\ 0.8)
\end{aligned}
$$

**Step 3 — The dot products.** Cosine similarity is now just multiply and add:

$$
\begin{aligned}
\hat{\mathbf{q}} \cdot \hat{D}_1 &\approx 0.707 \cdot 0.667 + 0.707 \cdot 0.667 + 0 \\
&\approx 0.472 + 0.472 \approx 0.94
\end{aligned}
$$

$$
\begin{aligned}
\hat{\mathbf{q}} \cdot \hat{D}_2 &\approx 0.707 \cdot 0 + 0.707 \cdot 0.6 + 0 \cdot 0.8 \\
&\approx 0.42
\end{aligned}
$$

**Why this arrangement?** With millions of documents it pays off: the documents are normalised and stored once, each search only normalises the query, and what is left is multiply and add.

**Answer:** $0.94$ and $0.42$; $D_1$ is more similar.
