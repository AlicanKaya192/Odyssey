A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. Is it in the span?

**Question:** Is $(5, 7)$ in the span of $(1, 2)$ and $(2, 3)$? If so, what are the coefficients?

$c_1(1, 2) + c_2(2, 3) = (5, 7)$:

$$
\begin{aligned}
c_1 + 2c_2 &= 5 \\
2c_1 + 3c_2 &= 7
\end{aligned}
$$

From the first, $c_1 = 5 - 2c_2$; put it into the second: $10 - 4c_2 +
3c_2 = 7$, so $c_2 = 3$ and $c_1 = -1$.

Check: $-1 \cdot (1, 2) + 3 \cdot (2, 3) = (-1 + 6,\ -2 + 9) = (5, 7)$ ✓.

We could have said "yes" without any calculation: $(1, 2)$ and $(2, 3)$
point in different directions, so they span the whole plane.

## 2. Are three vectors independent?

**Question:** Are $(1, 1, 0)$, $(0, 1, 1)$, $(1, 2, 1)$ independent?

Make the vectors columns and eliminate. $R_2 - R_1$, then $R_3 - R_2$:

$$
\begin{bmatrix} 1 & 0 & 1 \\ 1 & 1 & 2 \\ 0 & 1 & 1 \end{bmatrix}
\to
\begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 0 & 1 & 1 \end{bmatrix}
\to
\begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 0 & 0 & 0 \end{bmatrix}
$$

Column 3 has no pivot: **dependent**. Indeed the third vector is the sum
of the first two: $(1, 1, 0) + (0, 1, 1) = (1, 2, 1)$.

## 3. The k that makes them dependent

**Question:** For which values of $k$ are $(1, k)$ and $(k, 4)$ dependent?

Two vectors; build the square matrix and set its determinant to zero:

$$
\det \begin{bmatrix} 1 & k \\ k & 4 \end{bmatrix} = 4 - k^2 = 0
$$

$k = 2$ or $k = -2$. For $k = 2$: $(1, 2)$ and $(2, 4)$; the second is
twice the first ✓. For $k = -2$: $(1, -2)$ and $(-2, 4)$; $-2$ times ✓.

## 4. Coordinates in another basis

**Question:** What are the coordinates of $(4, 5)$ in the basis
$\mathbf{b}_1 = (1, 2)$, $\mathbf{b}_2 = (1, -1)$?

$$
\begin{aligned}
c_1 + c_2 &= 4 \\
2c_1 - c_2 &= 5
\end{aligned}
$$

Add: $3c_1 = 9$, $c_1 = 3$; then $c_2 = 1$.

Check: $3(1, 2) + 1(1, -1) = (4, 5)$ ✓. The new coordinates are $(3, 1)$.

## 5. Rank

**Question:** What are the rank and the dimension of the null space of this matrix?

$$
A = \begin{bmatrix} 1 & 2 & 0 & 1 \\ 2 & 4 & 1 & 4 \\ 3 & 6 & 1 & 5 \end{bmatrix}
$$

$R_2 - 2R_1$ and $R_3 - 3R_1$:

$$
\begin{bmatrix} 1 & 2 & 0 & 1 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 1 & 2 \end{bmatrix}
$$

$R_3 - R_2$ clears the last row. The pivots are in columns 1 and 3:
$\operatorname{rank} A = 2$. By rank–nullity the null space has dimension
$4 - 2 = 2$.

## 6. A basis of the null space

**Question:** Find the null space of $A$ from example 5.

The equations of the echelon form:

$$
\begin{aligned}
x_1 + 2x_2 + x_4 &= 0 \\
x_3 + 2x_4 &= 0
\end{aligned}
$$

The free variables are $x_2 = s$, $x_4 = t$. The other two:
$x_3 = -2t$, $x_1 = -2s - t$.

$$
\mathbf{x} = s \begin{bmatrix} -2 \\ 1 \\ 0 \\ 0 \end{bmatrix} + t \begin{bmatrix} -1 \\ 0 \\ -2 \\ 1 \end{bmatrix}
$$

These two vectors form a basis of the null space (dimension 2 ✓). Check:
$A(-1, 0, -2, 1) = (-1 + 0 + 0 + 1,\ -2 + 0 - 2 + 4,\ -3 + 0 - 2 + 5) = (0, 0, 0)$ ✓.
