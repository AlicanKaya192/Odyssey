**Idea:** Column $j$ of the Jacobian is how the outputs change when only input $j$ changes a little. Take a small step and divide the difference by the step.

**Step 1 — The first column.** Increase $x$ by $0.01$: $F(1.01, 2) = (2.0402, \ 7.01)$, $F(1, 2) = (2, 7)$. The difference over $0.01$: $(4.02, \ 1) \approx (4, 1)$.

**Step 2 — The second column.** Increase $y$ by $0.01$: $F(1, 2.01) = (2.01, \ 7.03)$. The difference over $0.01$: $(1, 3)$.

**Step 3 — The determinant.** $\begin{bmatrix} 4 & 1 \\ 1 & 3 \end{bmatrix}$: $12 - 1 = 11$.

**Why the same result?** The partial derivative is exactly the limit of this ratio; the extra in $4.02$ comes from the finite step (it goes to $4$ as $h \to 0$). This is gradient checking for Jacobians: a Jacobian written in code can be verified column by column like this.

**Answer:** $4$, $1$, $11$.
