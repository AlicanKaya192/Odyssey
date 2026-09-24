**Idea:** Since $X^\mathsf{T}X = \begin{bmatrix} \mathbf{c}_1 \cdot \mathbf{c}_1 & \mathbf{c}_1 \cdot \mathbf{c}_2 \\ \mathbf{c}_2 \cdot \mathbf{c}_1 & \mathbf{c}_2 \cdot \mathbf{c}_2 \end{bmatrix}$, its determinant is

$$
\|\mathbf{c}_1\|^2 \, \|\mathbf{c}_2\|^2 - (\mathbf{c}_1 \cdot \mathbf{c}_2)^2
$$

Putting in the geometric meaning of the dot product ($\mathbf{c}_1 \cdot \mathbf{c}_2 = \|\mathbf{c}_1\|\|\mathbf{c}_2\|\cos\theta$):

$$
\det(X^\mathsf{T}X) = \|\mathbf{c}_1\|^2 \, \|\mathbf{c}_2\|^2 \,(1 - \cos^2\theta)
$$

The determinant depends on the angle between the columns. If $\cos^2\theta = 1$ (the columns lie on one line), it is zero.

**Step 1 — $X_1$: no calculation needed.** $\mathbf{c}_2 = (2, 4, 6) = 2\,\mathbf{c}_1$. The columns point the same way, $\theta = 0$, $\cos\theta = 1$. So

$$
\det(X_1^\mathsf{T}X_1) = 0
$$

**Step 2 — $X_2$: with the formula.** $\|\mathbf{c}_1\|^2 = 14$, $\|\mathbf{c}_2\|^2 = 4 + 16 + 49 = 69$, $\mathbf{c}_1 \cdot \mathbf{c}_2 = 2 + 8 + 21 = 31$:

$$
\begin{aligned}
\det(X_2^\mathsf{T}X_2) &= 14 \cdot 69 - 31^2 \\
&= 966 - 961 = 5
\end{aligned}
$$

**Step 3 — Look at the angle.** $\cos\theta = \dfrac{31}{\sqrt{14 \cdot 69}} \approx \dfrac{31}{31.08} \approx 0.997$. The angle between the columns is about $4°$: almost the same direction.

**Why does it matter?** This route shows **why** the determinant is small: the two features measure almost the same thing. In real data this is the problem called multicollinearity; the fix is either to drop one of the features or to add $\lambda$ to the diagonal with ridge.

**Answer:** $0$ and $5$.
