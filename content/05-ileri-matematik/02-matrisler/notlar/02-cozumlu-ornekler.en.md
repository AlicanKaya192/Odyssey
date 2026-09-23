A worked example, step by step, for each method in the lesson. Try the question yourself first, then read the solution.

## 1. Reading size and entries

**Question:** What is the size of the matrix below? What are $b_{12}$ and $b_{23}$?

$$
B = \begin{bmatrix} 4 & -1 & 0 \\ 2 & 6 & 3 \end{bmatrix}
$$

2 rows, 3 columns: the size is $2 \times 3$.

- $b_{12}$: row 1, column 2 $\Rightarrow -1$
- $b_{23}$: row 2, column 3 $\Rightarrow 3$

There is **no** entry $b_{32}$: there is no row 3.

## 2. Finding unknowns from equality

**Question:** What are $x$ and $y$?

$$
\begin{bmatrix} x + 1 & 4 \\ 3 & 2y \end{bmatrix} = \begin{bmatrix} 5 & 4 \\ 3 & -6 \end{bmatrix}
$$

Corresponding entries must be equal:

$$
x + 1 = 5 \;\Rightarrow\; x = 4
$$

$$
2y = -6 \;\Rightarrow\; y = -3
$$

## 3. A linear combination

**Question:** For $A = \begin{bmatrix} 1 & 0 \\ 2 & -1 \end{bmatrix}$ and $B = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix}$, what is $2A - 3B$?

Scale first:

$$
2A = \begin{bmatrix} 2 & 0 \\ 4 & -2 \end{bmatrix}
\qquad
3B = \begin{bmatrix} 0 & 3 \\ 3 & 3 \end{bmatrix}
$$

Then subtract entry by entry:

$$
2A - 3B = \begin{bmatrix} 2 & -3 \\ 1 & -5 \end{bmatrix}
$$

## 4. The transpose

**Question:** If $C = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}$, what is $C^\mathsf{T}$?

$C$ is $3 \times 2$, so $C^\mathsf{T}$ is $2 \times 3$. The columns of $C$
become the rows of $C^\mathsf{T}$:

$$
C^\mathsf{T} = \begin{bmatrix} 1 & 3 & 5 \\ 2 & 4 & 6 \end{bmatrix}
$$

Check: $(C^\mathsf{T})_{13} = 5$ and $c_{31} = 5$. ✓

## 5. Values that make it symmetric

**Question:** The matrix is symmetric. What are $x$ and $y$?

$$
S = \begin{bmatrix} 1 & x & 4 \\ 3 & 2 & y \\ 4 & 5 & 0 \end{bmatrix}
$$

In a symmetric matrix $s_{ij} = s_{ji}$:

- $s_{12} = s_{21}$: $x = 3$
- $s_{23} = s_{32}$: $y = 5$
- $s_{13} = s_{31}$: $4 = 4$ ✓ (already satisfied)

## 6. Matrix times vector, both views

**Question:** What is $\begin{bmatrix} 3 & 0 & -1 \\ 1 & 2 & 2 \end{bmatrix} \begin{bmatrix} 2 \\ 1 \\ 4 \end{bmatrix}$?

Sizes: $(2 \times 3)$ times 3 components, so the result has 2 components.

**Row view:**

$$
\begin{bmatrix} 3 \cdot 2 + 0 \cdot 1 + (-1) \cdot 4 \\ 1 \cdot 2 + 2 \cdot 1 + 2 \cdot 4 \end{bmatrix}
= \begin{bmatrix} 2 \\ 12 \end{bmatrix}
$$

**Column view:**

$$
2 \begin{bmatrix} 3 \\ 1 \end{bmatrix} + 1 \begin{bmatrix} 0 \\ 2 \end{bmatrix} + 4 \begin{bmatrix} -1 \\ 2 \end{bmatrix}
= \begin{bmatrix} 6 + 0 - 4 \\ 2 + 2 + 8 \end{bmatrix}
= \begin{bmatrix} 2 \\ 12 \end{bmatrix}
$$

## 7. All predictions in one product

**Question:** Two students' (study hours, sleep hours) and a model's
weights:

$$
X = \begin{bmatrix} 5 & 7 \\ 2 & 8 \end{bmatrix}
\qquad
\mathbf{w} = \begin{bmatrix} 10 \\ 2 \end{bmatrix}
$$

What score does the model predict for the two students?

$$
X\mathbf{w} = \begin{bmatrix} 5 \cdot 10 + 7 \cdot 2 \\ 2 \cdot 10 + 8 \cdot 2 \end{bmatrix} = \begin{bmatrix} 64 \\ 36 \end{bmatrix}
$$

Every row is a student and every prediction is that row's dot product with $\mathbf{w}$.

## 8. Is the product defined?

**Question:** $A$ is a $3 \times 2$ matrix and $\mathbf{x}$ a vector with 3
components. Are $A\mathbf{x}$ and $A^\mathsf{T}\mathbf{x}$ defined?

- $A\mathbf{x}$: $A$ has 2 columns, $\mathbf{x}$ has 3 components. **Undefined.**
- $A^\mathsf{T}$ is $2 \times 3$: it has 3 columns and $\mathbf{x}$ has 3 components. **Defined**, with a 2-component result.

That is exactly why $X^\mathsf{T}$ shows up so often in machine learning:
when the data matrix needs to be read "per feature", it is transposed.
