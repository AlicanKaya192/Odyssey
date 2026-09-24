**What is asked?** The direction in which $A$ sends the point $\mathbf{v}_1$ of the circle: the direction of the ellipse's longest axis.

**Idea:** The basic SVD relation is $A\mathbf{v}_i = \sigma_i\mathbf{u}_i$. Computing $A\mathbf{v}_1$ and dividing by $\sigma_1$ gives $\mathbf{u}_1$.

**Step 1 — $A\mathbf{v}_1$.** Keep the factor $\tfrac{1}{\sqrt{2}}$ outside:

$$
A \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 3 \\ 4 + 5 \end{bmatrix} = \begin{bmatrix} 3 \\ 9 \end{bmatrix}
$$

So $A\mathbf{v}_1 = \tfrac{1}{\sqrt{2}}(3, 9)$.

**Step 2 — Divide by $\sigma_1$.** $\sigma_1 = 3\sqrt{5}$:

$$
\begin{aligned}
\mathbf{u}_1 &= \frac{1}{3\sqrt{5}} \cdot \frac{1}{\sqrt{2}} \begin{bmatrix} 3 \\ 9 \end{bmatrix} \\
&= \frac{1}{\sqrt{10}} \begin{bmatrix} 1 \\ 3 \end{bmatrix}
\end{aligned}
$$

**Step 3 — Turn it into numbers.** $\sqrt{10} \approx 3.162$:

$$
\mathbf{u}_1 \approx (0.316,\ 0.949)
$$

**Check:** Is it a unit vector? $\tfrac{1}{10}(1 + 9) = 1$ ✓. Is the length of $A\mathbf{v}_1$ really $\sigma_1$? $\tfrac{1}{\sqrt{2}}\sqrt{9 + 81} = \tfrac{\sqrt{90}}{\sqrt{2}} = \sqrt{45} = 3\sqrt{5}$ ✓.

**Reading the result:** The ellipse's longest axis points along $(1, 3)$, about $72°$ above the horizontal. The input direction $\mathbf{v}_1$ was at $45°$: $A$ both rotated and stretched it.

**Answer:** $\mathbf{u}_1 \approx (0.32,\ 0.95)$.
