The short version of everything in the lesson. Come back here when you get stuck on a question.

## Notation

| Concept | Meaning |
|---|---|
| $A\mathbf{x} = \mathbf{b}$ | Coefficient matrix, unknowns, right-hand side |
| $[A \mid \mathbf{b}]$ | Augmented matrix: each row is an equation |
| $R_i$ | Row $i$ |
| Pivot | The first non-zero entry of a row in echelon form |
| Free variable | The unknown of a column without a pivot |

## Row operations (they keep the solutions)

| Operation | Effect on the determinant |
|---|---|
| $R_i \leftrightarrow R_j$ | the sign flips |
| $R_i \to c\,R_i$, $c \ne 0$ | multiplied by $c$ |
| $R_i \to R_i + c\,R_j$ | unchanged |

Each operation is applied to the **whole row**, right-hand side included.

## Gaussian elimination

1. Go column by column; if the pivot is zero, swap with a lower row.
2. For each row below the pivot, $R_i \to R_i - \dfrac{a_{i\,k}}{\text{pivot}}\,R_k$.
3. Once in echelon form, start at the bottom and **back-substitute**.
4. Test your solution in the **original** equations.

## Reading the result

| After elimination | Solutions |
|---|---|
| Every unknown's column has a pivot | one |
| $[\,0 \;\cdots\; 0 \mid c\,]$, $c \ne 0$ | none (inconsistent) |
| No $0 = c$ row, but a column without a pivot | infinitely many; free variable $= t$ |

A linear system can have **only** 0, 1 or infinitely many solutions.

For a square system: $\det A \ne 0 \iff$ exactly one solution.

## Gauss–Jordan

- Make the pivots $1$, clear both below and above them.
- The solution is read directly from the last column.
- Inverse: $[A \mid I] \to [I \mid A^{-1}]$. If the left side cannot become $I$, there is no inverse.

## The determinant by elimination

$$
\det A = (-1)^{\text{number of swaps}} \cdot (\text{product of the pivots})
$$

(when only additions and swaps were used)

## Computational cost

| Method | Rough work for $n \times n$ |
|---|---|
| Gaussian elimination | $n^3 / 3$ |
| Inverting, then multiplying | $n^3$ |
| Determinant by expansion | $n!$ |

## Practical tips

- Put an equation with pivot $1$ in the first row (swap if needed); you avoid fractions.
- Write the operation you did ($R_2 - 2R_1$ and so on) next to each step.
- To avoid fractions you may first multiply a row by a whole number.
- With infinitely many solutions, write the answer with a parameter: $(-1 + t,\ 3 - 2t,\ t)$.
