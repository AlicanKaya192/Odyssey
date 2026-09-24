A worked example for each method in the lesson. Try the question yourself first, then read the solution.

## 1. A system in two unknowns

**Question:** Solve the system $2x - y = 3$ and $x + 4y = -3$ by elimination.

The augmented matrix; we swap the rows to put the equation with pivot $1$
on top:

$$
\left[\begin{array}{cc|c} 2 & -1 & 3 \\ 1 & 4 & -3 \end{array}\right]
\xrightarrow{R_1 \leftrightarrow R_2}
\left[\begin{array}{cc|c} 1 & 4 & -3 \\ 2 & -1 & 3 \end{array}\right]
$$

$R_2 \to R_2 - 2R_1$:

$$
\left[\begin{array}{cc|c} 1 & 4 & -3 \\ 0 & -9 & 9 \end{array}\right]
$$

Back substitution: $-9y = 9 \Rightarrow y = -1$; $x + 4 \cdot (-1) = -3
\Rightarrow x = 1$.

Check: $2 \cdot 1 - (-1) = 3$ ✓, $1 + 4 \cdot (-1) = -3$ ✓.

## 2. A zero pivot

**Question:** Solve the system $y + z = 3$, $x + y + z = 4$, $2x + y + 3z = 9$.

The first entry of the first row is $0$: it cannot be a pivot. Swap rows 1
and 2:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & 1 & 3 \\ 2 & 1 & 3 & 9 \end{array}\right]
$$

$R_3 \to R_3 - 2R_1$, then $R_3 \to R_3 + R_2$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & 1 & 3 \\ 0 & -1 & 1 & 1 \end{array}\right]
\;\to\;
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 4 \\ 0 & 1 & 1 & 3 \\ 0 & 0 & 2 & 4 \end{array}\right]
$$

$2z = 4 \Rightarrow z = 2$; $y + 2 = 3 \Rightarrow y = 1$;
$x + 1 + 2 = 4 \Rightarrow x = 1$.

## 3. A system with no solution

**Question:** Does the system $x + 2y = 4$ and $3x + 6y = 10$ have a solution?

$R_2 \to R_2 - 3R_1$:

$$
\left[\begin{array}{cc|c} 1 & 2 & 4 \\ 0 & 0 & -2 \end{array}\right]
$$

The last row says $0 = -2$: impossible. **No solution.** Geometrically the
two lines are parallel: the left side of the second equation is 3 times
the first, but the right side ($10$) is not $3 \cdot 4 = 12$.

## 4. Infinitely many solutions

**Question:** Find all solutions of the system $x + y - z = 1$ and $2x + 3y + z = 6$.

Two equations, three unknowns. $R_2 \to R_2 - 2R_1$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & -1 & 1 \\ 0 & 1 & 3 & 4 \end{array}\right]
$$

Column 3 has no pivot: $z$ is free, $z = t$.

$$
\begin{aligned}
y &= 4 - 3t \\
x &= 1 - y + z = 1 - (4 - 3t) + t = -3 + 4t
\end{aligned}
$$

The solution set is $(-3 + 4t,\ 4 - 3t,\ t)$. For a check take $t = 0$:
$(-3, 4, 0)$; $-3 + 4 - 0 = 1$ ✓, $-6 + 12 + 0 = 6$ ✓.

## 5. The inverse with Gauss–Jordan

**Question:** Find the inverse of $A = \begin{bmatrix} 2 & 3 \\ 1 & 2 \end{bmatrix}$
with the $[A \mid I]$ method.

$$
\left[\begin{array}{cc|cc} 2 & 3 & 1 & 0 \\ 1 & 2 & 0 & 1 \end{array}\right]
\xrightarrow{R_1 \leftrightarrow R_2}
\left[\begin{array}{cc|cc} 1 & 2 & 0 & 1 \\ 2 & 3 & 1 & 0 \end{array}\right]
$$

$$
\xrightarrow{R_2 - 2R_1}
\left[\begin{array}{cc|cc} 1 & 2 & 0 & 1 \\ 0 & -1 & 1 & -2 \end{array}\right]
\xrightarrow{-R_2}
\left[\begin{array}{cc|cc} 1 & 2 & 0 & 1 \\ 0 & 1 & -1 & 2 \end{array}\right]
$$

$$
\xrightarrow{R_1 - 2R_2}
\left[\begin{array}{cc|cc} 1 & 0 & 2 & -3 \\ 0 & 1 & -1 & 2 \end{array}\right]
$$

$A^{-1} = \begin{bmatrix} 2 & -3 \\ -1 & 2 \end{bmatrix}$. Check with the
formula: $\det A = 4 - 3 = 1$; swap and flip signs: the same matrix. ✓

## 6. The determinant by elimination

**Question:** What is $\det \begin{bmatrix} 2 & 1 & 3 \\ 4 & 5 & 7 \\ -2 & 2 & 1 \end{bmatrix}$?

Bring it to echelon form using additions only.
$R_2 \to R_2 - 2R_1$, $R_3 \to R_3 + R_1$:

$$
\begin{bmatrix} 2 & 1 & 3 \\ 0 & 3 & 1 \\ 0 & 3 & 4 \end{bmatrix}
$$

$R_3 \to R_3 - R_2$:

$$
\begin{bmatrix} 2 & 1 & 3 \\ 0 & 3 & 1 \\ 0 & 0 & 3 \end{bmatrix}
$$

No swaps; the determinant is the product of the pivots: $2 \cdot 3 \cdot 3 = 18$.
