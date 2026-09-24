**Idea:** Find the dropped energy first; the share kept is $1 - (\text{share dropped})$. The error is directly the square root of the dropped energy. Both questions come from the same number ($9 + 1$).

**Step 1 — The dropped energy.** $\sigma_3^2 + \sigma_4^2 = 9 + 1 = 10$.

**Step 2 — The total energy.** $144 + 25 + 9 + 1 = 179$.

**Step 3 — The share dropped.**

$$
\frac{10}{179} \approx 0.056
$$

**Step 4 — The share kept.**

$$
1 - 0.056 = 0.944 \approx 0.94
$$

**Step 5 — The error.** The square root of the dropped energy: $\sqrt{10} \approx 3.16$.

**Reading the result:** The "size" of the matrix is $\sqrt{179} \approx 13.4$; the error is $3.16$. The relative error is $3.16 / 13.4 \approx 0.24$, so the entries deviate by about 24% on average. The energy share (94%) looks more optimistic than the error because it works with squares.

**Why the same result?** Both routes rest on $\|A\|^2 = \|A_2\|^2 + \|A - A_2\|^2$; the layers are perpendicular to each other, so their energies add up.

**Answer:** $0.94$ and $3.16$.
