A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. Determinant and area

**Question:** $A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ is applied to a triangle of area 3. What is the area of the new triangle?

$$
\det A = 4 \cdot 3 - 1 \cdot 2 = 12 - 2 = 10
$$

The determinant is the area factor: every shape's area grows 10 times.
The new area is $3 \cdot 10 = 30$.

## 2. A 3 × 3 determinant using the zeros

**Question:** What is $\det \begin{bmatrix} 3 & 0 & 2 \\ 1 & 0 & 4 \\ 2 & 5 & 1 \end{bmatrix}$?

Column 2 has two zeros; expand along it. The only non-zero entry is $5$,
in row 3, column 2. In the sign pattern that position is $-$ (row 3,
column 2 of $+ - +$ / $- + -$ / $+ - +$).

Deleting the row and column of the $5$ leaves:

$$
\begin{vmatrix} 3 & 2 \\ 1 & 4 \end{vmatrix} = 12 - 2 = 10
$$

$$
\det = -5 \cdot 10 = -50
$$

Expanding along the first row would need three terms; the result is the
same.

## 3. Is there an inverse?

**Question:** Does $\begin{bmatrix} 2 & 6 \\ 1 & 3 \end{bmatrix}$ have an inverse?

$$
\det = 2 \cdot 3 - 6 \cdot 1 = 0
$$

No. You can see why: column 2, $(6, 3)$, is 3 times column 1, $(2, 1)$.
The two columns lie on one line and the plane is squashed onto it.

## 4. A 2 × 2 inverse

**Question:** What is the inverse of $A = \begin{bmatrix} 5 & 2 \\ 2 & 1 \end{bmatrix}$?

Determinant first: $5 \cdot 1 - 2 \cdot 2 = 1$. Not zero, so the inverse exists.

Swap, flip signs, divide by $1$:

$$
A^{-1} = \frac{1}{1} \begin{bmatrix} 1 & -2 \\ -2 & 5 \end{bmatrix} = \begin{bmatrix} 1 & -2 \\ -2 & 5 \end{bmatrix}
$$

Check:

$$
\begin{bmatrix} 5 & 2 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} 1 & -2 \\ -2 & 5 \end{bmatrix} = \begin{bmatrix} 5 - 4 & -10 + 10 \\ 2 - 2 & -4 + 5 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
$$

With determinant $1$ the inverse has whole-number entries too.

## 5. Solving a system with the inverse

**Question:** Solve the system $5x + 2y = 4$ and $2x + y = 1$.

In matrix form $A\mathbf{x} = \mathbf{b}$, with $A$ from example 4 and
$\mathbf{b} = (4, 1)$. The inverse is ready:

$$
\mathbf{x} = A^{-1}\mathbf{b} = \begin{bmatrix} 1 & -2 \\ -2 & 5 \end{bmatrix} \begin{bmatrix} 4 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 - 2 \\ -8 + 5 \end{bmatrix} = \begin{bmatrix} 2 \\ -3 \end{bmatrix}
$$

Check: $5 \cdot 2 + 2 \cdot (-3) = 4$ ✓, $2 \cdot 2 + (-3) = 1$ ✓.

## 6. Determinants from the rules

**Question:** $A$ is $3 \times 3$ with $\det A = 3$. What are $\det(2A)$, $\det(A^\mathsf{T})$, $\det(A^{-1})$ and $\det(A^2)$?

- $\det(2A) = 2^3 \cdot 3 = 24$ (each of the three dimensions doubles)
- $\det(A^\mathsf{T}) = \det A = 3$
- $\det(A^{-1}) = \dfrac{1}{3}$
- $\det(A^2) = \det A \cdot \det A = 9$

None of them needed the entries of $A$.

## 7. Undoing transformations in a row

**Question:** A shape is first stretched by 2 in the $x$ direction ($S$),
then rotated by $90°$ ($R$). Which transformation undoes this?

The total transformation is $RS$. Its inverse is $(RS)^{-1} =
S^{-1}R^{-1}$: **first** undo $R$ (rotate by $-90°$), **then** undo $S$
(halve $x$).

$$
R^{-1} = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}
\qquad
S^{-1} = \begin{bmatrix} 0.5 & 0 \\ 0 & 1 \end{bmatrix}
$$

$$
S^{-1}R^{-1} = \begin{bmatrix} 0.5 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 0.5 \\ -1 & 0 \end{bmatrix}
$$

Check: $RS = \begin{bmatrix} 0 & -1 \\ 2 & 0 \end{bmatrix}$ and
$\begin{bmatrix} 0 & 0.5 \\ -1 & 0 \end{bmatrix} \begin{bmatrix} 0 & -1 \\ 2 & 0 \end{bmatrix} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$. ✓
