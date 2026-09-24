**What is asked?** The gain from SVD compression: how many numbers are needed to store the first 30 layers instead of the original?

**Idea:** The rank-$k$ approximation is $A_k = \sum_{i=1}^{k} \sigma_i\mathbf{u}_i\mathbf{v}_i^\mathsf{T}$. We do not store the matrix itself but the three pieces of each layer: $\mathbf{u}_i$ (as many numbers as rows), $\mathbf{v}_i$ (as many as columns) and $\sigma_i$ (one number).

**Step 1 — One layer.** $m = 400$, $n = 600$:

$$
m + n + 1 = 400 + 600 + 1 = 1001 \text{ numbers}
$$

**Step 2 — 30 layers.**

$$
k\,(m + n + 1) = 30 \cdot 1001 = 30\,030
$$

**Step 3 — The original.** One number per pixel:

$$
m \cdot n = 400 \cdot 600 = 240\,000
$$

**Step 4 — The ratio.**

$$
\frac{30\,030}{240\,000} \approx 0.1251 \quad \Rightarrow \quad 12.5\%
$$

**Reading the result:** Less than an eighth of the original. In real photos the singular values shrink fast, so 30 layers usually keep the photo good enough for the eye to recognise easily; the lost detail is in the smallest layers.

**Watch out:** Computing $k \cdot m \cdot n$ would be wrong: if you rebuild $A_k$ as a full matrix and store it, you still store $240\,000$ numbers. The gain comes from storing the pieces of the layers separately.

**Answer:** $30\,030$ numbers; about 12.5%.
