A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. Is the product defined, and what size is it?

**Question:** Let $A$ be $3 \times 2$, $B$ be $2 \times 4$ and $C$ be
$4 \times 3$. What are the sizes of $AB$, $BA$, $BC$ and $ABC$?

- $AB$: $(3 \times 2)(2 \times 4)$, inner numbers $2 = 2$. Result $3 \times 4$.
- $BA$: $(2 \times 4)(3 \times 2)$, inner numbers $4 \ne 3$. **Undefined.**
- $BC$: $(2 \times 4)(4 \times 3)$, result $2 \times 3$.
- $ABC$: $AB$ is $3 \times 4$, times $C$ ($4 \times 3$): result $3 \times 3$.

## 2. Computing a product entry by entry

**Question:** What is $AB$?

$$
A = \begin{bmatrix} 1 & -1 & 2 \\ 0 & 3 & 1 \end{bmatrix}
\qquad
B = \begin{bmatrix} 2 & 1 \\ 1 & 0 \\ -1 & 4 \end{bmatrix}
$$

$(2 \times 3)(3 \times 2)$: the result is $2 \times 2$. Each entry is the
dot product of a row and a column:

$$
\begin{aligned}
c_{11} &= 1 \cdot 2 + (-1) \cdot 1 + 2 \cdot (-1) = 2 - 1 - 2 = -1 \\
c_{12} &= 1 \cdot 1 + (-1) \cdot 0 + 2 \cdot 4 = 1 + 0 + 8 = 9 \\
c_{21} &= 0 \cdot 2 + 3 \cdot 1 + 1 \cdot (-1) = 0 + 3 - 1 = 2 \\
c_{22} &= 0 \cdot 1 + 3 \cdot 0 + 1 \cdot 4 = 4
\end{aligned}
$$

$$
AB = \begin{bmatrix} -1 & 9 \\ 2 & 4 \end{bmatrix}
$$

## 3. Comparing $AB$ and $BA$

**Question:** For $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ and
$B = \begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix}$, what are $AB$ and $BA$?

$$
AB = \begin{bmatrix} 1 + 1 & 0 + 1 \\ 0 + 1 & 0 + 1 \end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}
$$

$$
BA = \begin{bmatrix} 1 + 0 & 1 + 0 \\ 1 + 0 & 1 + 1 \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix}
$$

They differ. When two shears (one horizontal, one vertical) are done in a
row, the order changes the result.

## 4. The transpose of a product

**Question:** For $A$ and $B$ from example 2, what is $B^\mathsf{T} A^\mathsf{T}$?

With the rule, no calculation is needed: $B^\mathsf{T} A^\mathsf{T} =
(AB)^\mathsf{T}$. We found $AB$ in example 2; taking its transpose is
enough:

$$
B^\mathsf{T} A^\mathsf{T} = \begin{bmatrix} -1 & 2 \\ 9 & 4 \end{bmatrix}
$$

## 5. Writing the matrix of a desired transformation

**Question:** Which matrix takes $\mathbf{e}_1$ to $(1, 1)$ and
$\mathbf{e}_2$ to $(-1, 1)$? Where does $(2, 0)$ go?

The destinations are the columns of the matrix:

$$
M = \begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix}
$$

$$
M \begin{bmatrix} 2 \\ 0 \end{bmatrix} = \begin{bmatrix} 2 \\ 2 \end{bmatrix}
$$

This matrix rotates everything by $45°$ and enlarges it $\sqrt{2}$ times:
the length of $(2, 0)$ is $2$, that of $(2, 2)$ is $2\sqrt{2}$.

## 6. Two transformations in a row

**Question:** First scale by 3 in the $x$ direction ($S$), then rotate by
$90°$ ($R$). What is the single matrix? Where does $(1, 2)$ go?

"First $S$, then $R$" $\Rightarrow RS$:

$$
RS = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ 3 & 0 \end{bmatrix}
$$

$$
RS \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} -2 \\ 3 \end{bmatrix}
$$

Step-by-step check: $S(1, 2) = (3, 2)$, then $R(3, 2) = (-2, 3)$. ✓

## 7. Taking powers

**Question:** For $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, what
are $A^2$ and $A^3$?

$$
A^2 = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}
$$

$$
A^3 = A^2 A = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 3 \\ 0 & 1 \end{bmatrix}
$$

Shearing three times is shearing three times as much. Squaring the
entries would have given $A^2 = A$ again, which is wrong.
