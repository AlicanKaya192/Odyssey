The short version of everything in the lesson. Come back here when a question stops you.

## Reading

| Concept | Meaning |
|---|---|
| Size $m \times n$ | $m$ rows, $n$ columns (rows first) |
| $a_{ij}$ | the entry in row $i$, column $j$ |
| $\mathbb{R}^{m \times n}$ | real matrices of size $m \times n$ |
| Column vector | an $n \times 1$ matrix; what "vector" means |
| Row vector | a $1 \times n$ matrix; $\mathbf{x}^\mathsf{T}$ |
| Diagonal | $a_{11}, a_{22}, \dots$ (square matrices only) |

## Special matrices

| Name | Condition |
|---|---|
| Square | $m = n$ |
| Zero $O$ | every entry $0$ |
| Diagonal | square, off-diagonal $0$ |
| Identity $I$ | diagonal, diagonal $1$ |
| Upper triangular | square, below the diagonal $0$ |
| Lower triangular | square, above the diagonal $0$ |
| Symmetric | $A^\mathsf{T} = A$, that is $a_{ij} = a_{ji}$ |

## Operations

| Operation | Rule | Size condition |
|---|---|---|
| $A + B$, $A - B$ | entry by entry | same size |
| $cA$ | every entry times $c$ | none |
| $A^\mathsf{T}$ | $(A^\mathsf{T})_{ij} = a_{ji}$ | $m \times n \to n \times m$ |
| $A\mathbf{x}$ | dot products with the rows | columns of $A$ = length of $\mathbf{x}$ |
| $\operatorname{tr} A$ | sum of the diagonal | square |

## Two views of the matrix–vector product

$$
A\mathbf{x} = \begin{bmatrix} \text{row 1} \cdot \mathbf{x} \\ \text{row 2} \cdot \mathbf{x} \\ \vdots \end{bmatrix}
$$

$$
A\mathbf{x} = x_1\,\mathbf{a}_1 + x_2\,\mathbf{a}_2 + \cdots + x_n\,\mathbf{a}_n
$$

The row view is for **computing**, the column view for **meaning**:
$A\mathbf{x}$ is always a linear combination of the columns of $A$.

## Rules

- $A + B = B + A$, $\;(A + B) + C = A + (B + C)$
- $c(A + B) = cA + cB$, $\;(c + d)A = cA + dA$
- $(A^\mathsf{T})^\mathsf{T} = A$, $\;(A + B)^\mathsf{T} = A^\mathsf{T} + B^\mathsf{T}$, $\;(cA)^\mathsf{T} = cA^\mathsf{T}$
- $A(\mathbf{x} + \mathbf{y}) = A\mathbf{x} + A\mathbf{y}$, $\;A(c\mathbf{x}) = c\,A\mathbf{x}$
- $I\mathbf{x} = \mathbf{x}$
- $\mathbf{a} \cdot \mathbf{b} = \mathbf{a}^\mathsf{T}\mathbf{b}$

## Practical tips

- Write the sizes under the product: $(2 \times 3)(3 \times 1)$. The two
  inner numbers must match; the two outer numbers are the size of the
  result.
- Before transposing, change the size first: if it is $2 \times 3$ the
  result will be $3 \times 2$; draw the empty table and fill it in.
- For symmetry look at one side of the diagonal only: does every $a_{ij}$
  equal $a_{ji}$ on the opposite side?
- In ML the rows of $X$ are examples and the columns features: $n \times d$.
