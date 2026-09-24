The short version of everything in the lesson. Come back here when you get stuck on a question.

## Determinant

$$
\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc
$$

$$
\det \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
= a(ei - fh) - b(di - fg) + c(dh - eg)
$$

| Value | Meaning |
|---|---|
| $\lvert\det A\rvert$ | By what factor area (in 3D, volume) changes |
| $\det A < 0$ | The orientation flipped (a mirror is involved) |
| $\det A = 0$ | The plane is squashed; the columns lie on one line; no inverse |
| $\det A = 1$ | Area is preserved (rotation, shear) |

**Sign pattern in an expansion:** $\begin{bmatrix} + & - & + \\ - & + & - \\ + & - & + \end{bmatrix}$. Pick the row or column with the most zeros.

**Triangular or diagonal matrix:** the determinant is the product of the diagonal.

## Rules of the determinant

| Rule | Result |
|---|---|
| $\det(AB)$ | $\det A \cdot \det B$ |
| $\det(A^\mathsf{T})$ | $\det A$ |
| $\det(cA)$, $A$ is $n \times n$ | $c^n \det A$ |
| $\det(A^{-1})$ | $1 / \det A$ |
| $\det I$ | $1$ |
| Swap two rows | the sign flips |
| Multiply a row by $c$ | $\det$ is multiplied by $c$ |
| Add a multiple of one row to another | unchanged |
| $\det(A + B)$ | **no rule** |

## The inverse matrix

$$
A A^{-1} = A^{-1} A = I
$$

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
$$

Swap ($a \leftrightarrow d$), flip signs ($-b$, $-c$), divide by the determinant.

| Rule | Result |
|---|---|
| Does an inverse exist? | if and only if $\det A \ne 0$ |
| $(A^{-1})^{-1}$ | $A$ |
| $(AB)^{-1}$ | $B^{-1} A^{-1}$ (order reversed) |
| $(A^\mathsf{T})^{-1}$ | $(A^{-1})^\mathsf{T}$ |
| $(cA)^{-1}$ | $\frac{1}{c} A^{-1}$ |

## Inverses of transformations

| Transformation | $\det$ | Inverse |
|---|---|---|
| Rotation by $\theta$ | $1$ | rotation by $-\theta$ |
| Reflection | $-1$ | itself |
| Scaling $\begin{bmatrix} s_1 & 0 \\ 0 & s_2 \end{bmatrix}$ | $s_1 s_2$ | $\begin{bmatrix} 1/s_1 & 0 \\ 0 & 1/s_2 \end{bmatrix}$ |
| Shear $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ | $1$ | $\begin{bmatrix} 1 & -k \\ 0 & 1 \end{bmatrix}$ |
| Projection | $0$ | none |

## Solving equations

$$
A\mathbf{x} = \mathbf{b} \quad \Rightarrow \quad \mathbf{x} = A^{-1}\mathbf{b}
$$

- $\det A \ne 0$: exactly one solution.
- $\det A = 0$: either no solution or infinitely many (Gaussian elimination section).
- Multiply by $A^{-1}$ **on the left**.

## Practical tips

- Compute the determinant before writing the inverse; if it is zero, stop.
- Leave $\frac{1}{\det}$ to the very end to avoid fractions.
- Always test the inverse you found with $AA^{-1} = I$; one product is enough.
- In a $3 \times 3$ determinant, if a row has two zeros, expand along it; one term is left.
- In ML, if $\det(X^\mathsf{T}X) \approx 0$, one column may be a repeat of the others.
