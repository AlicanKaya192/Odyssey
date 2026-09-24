**Idea:** For $2 \times 2$ we can make do with two facts without writing $A^\mathsf{T}A$:

- $\sigma_1^2 + \sigma_2^2$ = the sum of the squares of all entries of $A$,
- $\sigma_1 \sigma_2 = |\det A|$ (rotations do not change area; the area factor comes only from $\Sigma$).

Finding two numbers with a known sum and product is the same as the trace–determinant shortcut of the previous section.

**Step 1 — The sum of squares.**

$$
\sigma_1^2 + \sigma_2^2 = 3^2 + 0^2 + 4^2 + 5^2 = 50
$$

**Step 2 — The determinant.**

$$
\sigma_1\sigma_2 = |3 \cdot 5 - 0 \cdot 4| = 15
$$

So $\sigma_1^2 \sigma_2^2 = 225$.

**Step 3 — Find the squares.** $\sigma_1^2$ and $\sigma_2^2$ are two numbers with sum $50$ and product $225$: $45$ and $5$.

**Step 4 — Square roots.** $\sigma_1 = \sqrt{45} \approx 6.71$, $\sigma_2 = \sqrt{5} \approx 2.24$.

**Why the same result?** $\sigma_1^2 + \sigma_2^2 = \operatorname{tr}(A^\mathsf{T}A)$ and $\sigma_1^2\sigma_2^2 = \det(A^\mathsf{T}A)$. These are exactly the two numbers we used to build the characteristic equation in the first method; here we read them straight off $A$.

**Reading the result:** $A$ stretches one direction about $6.7$ times and the perpendicular direction only $2.2$ times. The condition number is $6.71 / 2.24 = 3$.

**Answer:** $6.71$ and $2.24$.
