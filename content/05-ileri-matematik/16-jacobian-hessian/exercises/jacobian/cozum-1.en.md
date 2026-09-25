**What is asked?** Two entries of the Jacobian of a vector function, and its determinant.

**Idea:** Row = output, column = input. Compute each entry as a partial derivative, then put in the point.

**Step 1 — The matrix.**

$$
J = \begin{bmatrix} 2xy & x^2 \\ 1 & 3 \end{bmatrix} \;\to\; \begin{bmatrix} 4 & 1 \\ 1 & 3 \end{bmatrix}
$$

**Step 2 — The determinant.** $4 \cdot 3 - 1 \cdot 1 = 11$.

**Check:** $\det J > 0$: at this point $F$ does not flip orientations, and it scales small areas by about $11$.

**Watch out:** $J_{12}$ is the derivative of the first output with respect to the **second input**: $\frac{\partial (x^2 y)}{\partial y} = x^2 = 1$. Mixing up rows and columns would give $J_{21} = 1$ instead; here it happens to be the same number, but not in general.

**Answer:** $4$, $1$ and $11$.
