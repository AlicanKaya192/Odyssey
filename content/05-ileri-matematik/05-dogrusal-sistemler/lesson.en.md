# Linear Systems and Gaussian Elimination

In the previous section we solved $A\mathbf{x} = \mathbf{b}$ with the
inverse matrix: $\mathbf{x} = A^{-1}\mathbf{b}$. A nice formula, but it
has two problems. First, computing the inverse of a large matrix is slow.
Second, when the determinant is zero the formula tells you nothing: does
the system have **no** solution, or **infinitely many**?

In this section we learn the method that answers both questions:
**Gaussian elimination**. It is the organised version, working in any
size, of the school method where you add two equations to get rid of an
unknown. It is also the method computers use to solve linear systems.

Prerequisite: the Determinants and Inverse Matrices section.

## What is a linear system?

Equations in which the unknowns appear only to the first power and are
never multiplied together are called **linear** equations. Several linear
equations together form a **linear system**:

$$
\begin{aligned}
x + y + z &= 6 \\
2x + 3y - z &= 5 \\
x - y + 2z &= 5
\end{aligned}
$$

With terms such as $x^2$, $xy$ or $\sin x$ the system would not be linear.

### Matrix form and the augmented matrix

The coefficients go into a matrix, the unknowns into a vector, the
right-hand sides into another vector: $A\mathbf{x} = \mathbf{b}$.

$$
\begin{bmatrix} 1 & 1 & 1 \\ 2 & 3 & -1 \\ 1 & -1 & 2 \end{bmatrix}
\begin{bmatrix} x \\ y \\ z \end{bmatrix}
= \begin{bmatrix} 6 \\ 5 \\ 5 \end{bmatrix}
$$

When solving by hand there is no need to rewrite $x, y, z$ on every line.
Appending the right-hand side to the coefficient matrix behind a bar gives
the **augmented matrix**:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & -1 & 5 \\ 1 & -1 & 2 & 5 \end{array}\right]
$$

Each row is an equation, each column left of the bar holds the
coefficients of one unknown, and the column on the right is the
right-hand side.

## Three possibilities

An equation in two unknowns is a line in the plane. The solution of a
system of two equations is the set of **common points** of the two lines.
Two lines can sit in three different ways:

<figure class="fig">
<svg viewBox="0 0 420 192" width="420"><line class="grid" x1="14" y1="134" x2="14" y2="14"/><line class="line" x1="38" y1="134" x2="38" y2="14"/><line class="grid" x1="62" y1="134" x2="62" y2="14"/><line class="grid" x1="86" y1="134" x2="86" y2="14"/><line class="grid" x1="110" y1="134" x2="110" y2="14"/><line class="grid" x1="134" y1="134" x2="134" y2="14"/><line class="grid" x1="14" y1="134" x2="134" y2="134"/><line class="line" x1="14" y1="110" x2="134" y2="110"/><line class="grid" x1="14" y1="86" x2="134" y2="86"/><line class="grid" x1="14" y1="62" x2="134" y2="62"/><line class="grid" x1="14" y1="38" x2="134" y2="38"/><line class="grid" x1="14" y1="14" x2="134" y2="14"/><line class="curve" x1="14" y1="14.0" x2="134" y2="134.0"/><line class="curve2" x1="38.0" y1="134" x2="134" y2="38.0"/><circle class="dot3" cx="86" cy="86" r="4.5"/><text class="ink" x="74.0" y="152" font-size="12" text-anchor="middle">One solution</text><text class="dim" x="74.0" y="168" font-size="11" text-anchor="middle">x + y = 3</text><text class="dim" x="74.0" y="182" font-size="11" text-anchor="middle">x − y = 1</text><line class="grid" x1="152" y1="134" x2="152" y2="14"/><line class="line" x1="176" y1="134" x2="176" y2="14"/><line class="grid" x1="200" y1="134" x2="200" y2="14"/><line class="grid" x1="224" y1="134" x2="224" y2="14"/><line class="grid" x1="248" y1="134" x2="248" y2="14"/><line class="grid" x1="272" y1="134" x2="272" y2="14"/><line class="grid" x1="152" y1="134" x2="272" y2="134"/><line class="line" x1="152" y1="110" x2="272" y2="110"/><line class="grid" x1="152" y1="86" x2="272" y2="86"/><line class="grid" x1="152" y1="62" x2="272" y2="62"/><line class="grid" x1="152" y1="38" x2="272" y2="38"/><line class="grid" x1="152" y1="14" x2="272" y2="14"/><line class="curve" x1="152" y1="14.0" x2="272" y2="134.0"/><line class="curve2" x1="152" y1="62.0" x2="224.0" y2="134"/><text class="ink" x="212.0" y="152" font-size="12" text-anchor="middle">No solution</text><text class="dim" x="212.0" y="168" font-size="11" text-anchor="middle">x + y = 3</text><text class="dim" x="212.0" y="182" font-size="11" text-anchor="middle">x + y = 1</text><line class="grid" x1="290" y1="134" x2="290" y2="14"/><line class="line" x1="314" y1="134" x2="314" y2="14"/><line class="grid" x1="338" y1="134" x2="338" y2="14"/><line class="grid" x1="362" y1="134" x2="362" y2="14"/><line class="grid" x1="386" y1="134" x2="386" y2="14"/><line class="grid" x1="410" y1="134" x2="410" y2="14"/><line class="grid" x1="290" y1="134" x2="410" y2="134"/><line class="line" x1="290" y1="110" x2="410" y2="110"/><line class="grid" x1="290" y1="86" x2="410" y2="86"/><line class="grid" x1="290" y1="62" x2="410" y2="62"/><line class="grid" x1="290" y1="38" x2="410" y2="38"/><line class="grid" x1="290" y1="14" x2="410" y2="14"/><line class="curve" x1="290" y1="38.0" x2="386.0" y2="134"/><line class="curve2" stroke-dasharray="6 5" x1="290" y1="38.0" x2="386.0" y2="134"/><text class="ink" x="350.0" y="152" font-size="12" text-anchor="middle">Infinitely many</text><text class="dim" x="350.0" y="168" font-size="11" text-anchor="middle">x + y = 2</text><text class="dim" x="350.0" y="182" font-size="11" text-anchor="middle">2x + 2y = 4</text></svg>
  <figcaption>On the left the lines meet at a single point: $(2, 1)$. In the middle they are parallel and never meet. On the right both equations describe the same line (the second is twice the first): every point on the line is a solution.</figcaption>
</figure>

| Case | Geometry | Number of solutions |
|---|---|---|
| The lines cross | one common point | **1** |
| The lines are parallel | no common point | **0** |
| The lines coincide | every point is common | **infinitely many** |

With three unknowns each equation is a **plane**, and the same three
cases apply: the planes meet at one point, have no common point at all,
or meet along a line (or plane). This holds in every dimension: **a linear
system has either 0, 1 or infinitely many solutions.** There is no linear
system with exactly two solutions.

The link to the determinant: for a square system, $\det A \ne 0$ means a
single solution. If $\det A = 0$ there is either no solution or infinitely
many; Gaussian elimination will tell us which.

## Row operations

Gaussian elimination turns the system into an easier one **without
changing its solutions**. Three operations are allowed for this:

| Operation | Written as | Why the solutions do not change |
|---|---|---|
| Swap | $R_i \leftrightarrow R_j$ | The order of the equations does not matter |
| Scale | $R_i \to c\,R_i$ ($c \ne 0$) | Multiplying both sides of an equation by the same number |
| Add | $R_i \to R_i + c\,R_j$ | Adding a multiple of one equation to another |

$R_i$ stands for row $i$. The third operation is the one used most: to
eliminate an unknown we subtract a suitable multiple of one row from
another.

**Rule:** An operation is applied to the **whole row** of the augmented
matrix, including the number to the right of the bar. Changing only the
left side breaks the equation.

## Gaussian elimination: two stages

### Stage 1: forward elimination

The goal is to **zero out everything below the diagonal**. The matrix then
reaches echelon form: each row contains fewer unknowns than the one above.

<figure class="fig">
<svg viewBox="0 0 400 186" width="400"><rect class="box" x="26" y="40" width="34" height="34"/><text class="ink" x="43.0" y="62.0" font-size="15" text-anchor="middle">■</text><rect class="box" x="60" y="40" width="34" height="34"/><text class="ink" x="77.0" y="62.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="94" y="40" width="34" height="34"/><text class="ink" x="111.0" y="62.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="128" y="40" width="34" height="34"/><text class="ink" x="145.0" y="62.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="26" y="74" width="34" height="34"/><text class="ink" x="43.0" y="96.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="60" y="74" width="34" height="34"/><text class="ink" x="77.0" y="96.0" font-size="15" text-anchor="middle">■</text><rect class="box" x="94" y="74" width="34" height="34"/><text class="ink" x="111.0" y="96.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="128" y="74" width="34" height="34"/><text class="ink" x="145.0" y="96.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="26" y="108" width="34" height="34"/><text class="ink" x="43.0" y="130.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="60" y="108" width="34" height="34"/><text class="ink" x="77.0" y="130.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="94" y="108" width="34" height="34"/><text class="ink" x="111.0" y="130.0" font-size="15" text-anchor="middle">■</text><rect class="box" x="128" y="108" width="34" height="34"/><text class="ink" x="145.0" y="130.0" font-size="15" text-anchor="middle">∗</text><rect class="curve" x="29" y="43" width="28" height="28" rx="4"/><rect class="curve" x="63" y="77" width="28" height="28" rx="4"/><rect class="curve" x="97" y="111" width="28" height="28" rx="4"/><line class="curve3" x1="128" y1="36" x2="128" y2="146" stroke-dasharray="4 3"/><path class="curve2" d="M26,74 H60 V108 H94 V142" fill="none"/><text class="ink" x="94" y="26" font-size="12" text-anchor="middle">Row echelon form</text><rect class="box" x="226" y="40" width="34" height="34"/><text class="ink" x="243.0" y="62.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="260" y="40" width="34" height="34"/><text class="ink" x="277.0" y="62.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="294" y="40" width="34" height="34"/><text class="ink" x="311.0" y="62.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="328" y="40" width="34" height="34"/><text class="ink" x="345.0" y="62.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="226" y="74" width="34" height="34"/><text class="ink" x="243.0" y="96.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="260" y="74" width="34" height="34"/><text class="ink" x="277.0" y="96.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="294" y="74" width="34" height="34"/><text class="ink" x="311.0" y="96.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="328" y="74" width="34" height="34"/><text class="ink" x="345.0" y="96.0" font-size="15" text-anchor="middle">∗</text><rect class="box" x="226" y="108" width="34" height="34"/><text class="ink" x="243.0" y="130.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="260" y="108" width="34" height="34"/><text class="ink" x="277.0" y="130.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="294" y="108" width="34" height="34"/><text class="ink" x="311.0" y="130.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="328" y="108" width="34" height="34"/><text class="ink" x="345.0" y="130.0" font-size="15" text-anchor="middle">∗</text><rect class="curve" x="229" y="43" width="28" height="28" rx="4"/><rect class="curve" x="263" y="77" width="28" height="28" rx="4"/><rect class="curve" x="297" y="111" width="28" height="28" rx="4"/><line class="curve3" x1="328" y1="36" x2="328" y2="146" stroke-dasharray="4 3"/><path class="curve2" d="M226,74 H260 V108 H294 V142" fill="none"/><text class="ink" x="294" y="26" font-size="12" text-anchor="middle">Reduced row echelon form</text><text class="dim" x="200" y="172" font-size="12" text-anchor="middle">■ pivot (non-zero), ∗ any number</text></svg>
  <figcaption>On the left, the echelon form forward elimination aims for: the first non-zero entry of each row (the pivot, framed) is to the right of the one above, and everything below the pivots is zero. On the right, the reduced form Gauss–Jordan aims for: pivots equal 1 and the rest of each pivot column is 0.</figcaption>
</figure>

For each column in turn:

1. **Choose the pivot:** the entry of that column in the row you are
   working on. If it is zero, swap with a lower row that has a non-zero
   entry.
2. **Clear below it:** from each row below the pivot, subtract the right
   multiple of the pivot row. Multiple $=$ (entry to be cleared) $/$
   (pivot).

Let us solve the system from the start of the section.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & -1 & 5 \\ 1 & -1 & 2 & 5 \end{array}\right]
$$

**Column 1.** The pivot is the $1$ in the top left. To clear the $2$ below
it, $R_2 \to R_2 - 2R_1$; for the $1$, $R_3 \to R_3 - R_1$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -3 & -7 \\ 0 & -2 & 1 & -1 \end{array}\right]
$$

The calculation on one line: $R_2 - 2R_1 = (2 - 2,\ 3 - 2,\ -1 - 2 \mid 5 - 12) = (0,\ 1,\ -3 \mid -7)$.

**Column 2.** The pivot is now the $1$ in row 2. To clear the $-2$ below
it, $R_3 \to R_3 + 2R_2$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -3 & -7 \\ 0 & 0 & -5 & -15 \end{array}\right]
$$

Everything below the diagonal is zero: echelon form. The last row is now
an equation in a single unknown.

### Stage 2: back substitution

We start at the bottom and work upwards:

$$
\begin{aligned}
-5z &= -15 &\Rightarrow\quad z &= 3 \\
y - 3z &= -7 &\Rightarrow\quad y &= -7 + 9 = 2 \\
x + y + z &= 6 &\Rightarrow\quad x &= 6 - 2 - 3 = 1
\end{aligned}
$$

**Check:** Put $(1, 2, 3)$ into the three original equations: $1 + 2 + 3 =
6$ ✓, $2 + 6 - 3 = 5$ ✓, $1 - 2 + 6 = 5$ ✓.

## No solution and infinitely many solutions

When elimination is finished, the last rows tell you the kind of system.

**No solution.** If a row becomes $\left[\begin{array}{ccc|c} 0 & 0 & 0 & c \end{array}\right]$
($c \ne 0$), that row says $0 = c$: impossible. Example:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 2 \\ 1 & 2 & 3 & 5 \\ 2 & 3 & 4 & 8 \end{array}\right]
\;\to\;
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 2 \\ 0 & 1 & 2 & 3 \\ 0 & 1 & 2 & 4 \end{array}\right]
\;\to\;
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 2 \\ 0 & 1 & 2 & 3 \\ 0 & 0 & 0 & 1 \end{array}\right]
$$

($R_2 - R_1$, $R_3 - 2R_1$, then $R_3 - R_2$.) The last row says $0 = 1$:
the system is **inconsistent** and has no solution. Geometrically there is
no point that lies on all three planes.

**Infinitely many solutions.** In the same system, change the last
right-hand side from $8$ to $7$. After elimination the last row becomes
$\left[\begin{array}{ccc|c} 0 & 0 & 0 & 0 \end{array}\right]$: $0 = 0$,
always true, saying nothing. What remains are **two** equations in three
unknowns:

$$
\begin{aligned}
x + y + z &= 2 \\
y + 2z &= 3
\end{aligned}
$$

The unknown of the column without a pivot ($z$) is a **free variable**:
we may give it any value. Setting $z = t$:

$$
\begin{aligned}
y &= 3 - 2t \\
x &= 2 - y - z = 2 - (3 - 2t) - t = -1 + t
\end{aligned}
$$

The solution set is $(x, y, z) = (-1 + t,\ 3 - 2t,\ t)$; one solution for
every number $t$. For $t = 0$ we get $(-1, 3, 0)$, for $t = 1$, $(0, 1,
1)$. Geometrically this is a **line**: the three planes meet along a line.

| After elimination | Meaning |
|---|---|
| Every column has a pivot | one solution |
| There is a $0 = c$ ($c \ne 0$) row | no solution |
| No $0 = c$ row, but a column without a pivot | infinitely many (one parameter per free variable) |

## Gauss–Jordan: finding the inverse

We can take elimination one step further: if we make the pivots $1$ (by
dividing the row by its pivot) and clear **above** the pivots too, back
substitution is no longer needed and the solution can be read straight
from the last column. This is called **Gauss–Jordan elimination**, and the
result is the **reduced row echelon form**.

The same method finds the inverse: write $I$ next to $A$ and turn the left
side into $I$; the right side becomes $A^{-1}$.

$$
[\,A \mid I\,] \;\longrightarrow\; [\,I \mid A^{-1}\,]
$$

Why? Every row operation is applied to both sides at once. The sequence
of operations that turns $A$ into $I$ is, as a matrix, the same as
multiplying by $A^{-1}$ on the left; the same sequence turns $I$ into
$A^{-1}I = A^{-1}$.

Example: $A = \begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix}$.

$$
\left[\begin{array}{cc|cc} 2 & 1 & 1 & 0 \\ 5 & 3 & 0 & 1 \end{array}\right]
\xrightarrow{R_1 / 2}
\left[\begin{array}{cc|cc} 1 & 0.5 & 0.5 & 0 \\ 5 & 3 & 0 & 1 \end{array}\right]
$$

$$
\xrightarrow{R_2 - 5R_1}
\left[\begin{array}{cc|cc} 1 & 0.5 & 0.5 & 0 \\ 0 & 0.5 & -2.5 & 1 \end{array}\right]
\xrightarrow{2R_2}
\left[\begin{array}{cc|cc} 1 & 0.5 & 0.5 & 0 \\ 0 & 1 & -5 & 2 \end{array}\right]
$$

$$
\xrightarrow{R_1 - 0.5R_2}
\left[\begin{array}{cc|cc} 1 & 0 & 3 & -1 \\ 0 & 1 & -5 & 2 \end{array}\right]
$$

$A^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}$; the same as with
the formula in the previous section. The difference: this method works
the same way for $3 \times 3$ and for $100 \times 100$. If the left side
cannot be turned into $I$ (a zero row appears), the matrix has no inverse.

## Finding the determinant by elimination

We saw the effect of row operations on the determinant in the previous
section: **adding** does not change it, **swapping** flips its sign. If we
reach echelon form using only additions (and swaps if needed), the echelon
form is triangular, so the determinant is the product of the diagonal:

$$
\det A = (\pm 1) \cdot (\text{product of the pivots})
$$

In the example at the start of the section we did no swaps and the pivots
are $1, 1, -5$: $\det A = 1 \cdot 1 \cdot (-5) = -5$. The $3 \times 3$
expansion gives the same; but for a $10 \times 10$ matrix the expansion
means 3.6 million terms, while elimination takes a few hundred operations.

## Why do computers use Gaussian elimination?

For an $n \times n$ system, elimination takes roughly $\tfrac{n^3}{3}$
multiplications. For $n = 1000$ that is about 330 million operations; a
tiny fraction of a second for a modern computer. Computing the inverse
and then multiplying is about three times as much work and more exposed
to rounding errors.

The "solve a system" functions of libraries (`solve` in NumPy) perform
elimination under the name **LU decomposition**: they store the
multipliers of forward elimination in a lower triangular matrix ($L$) and
the result in an upper triangular matrix ($U$), writing $A = LU$. When the
same $A$ must be solved for many different $\mathbf{b}$, elimination is
done only once.

**Partial pivoting:** in each column the computer picks the entry with the
**largest** absolute value as the pivot (swapping rows if necessary).
Dividing by a very small number magnifies rounding errors; picking the
largest prevents that.

## Linear systems in machine learning

**Finding a model's parameters.** Finding the parabola ($y = a + bx +
cx^2$) through three points is a linear system in three unknowns: the
unknowns are $a, b, c$ and each point is one equation. Even though $x^2$
appears, the system is linear **in $a, b, c$**. Linear regression rests on
the same idea: the weights are the solution of a linear system (the
normal equations).

**Less data than unknowns.** With 3 examples and 10 features there are 3
equations and 10 unknowns: infinitely many solutions. The model can find
infinitely many weight vectors that explain the data perfectly, but it
cannot know which one is really right. This is the linear-algebra face of
overfitting. Regularisation picks the one with the "smallest weights"
among these infinitely many solutions.

**More data than unknowns.** With 1000 houses and 3 features there are
1000 equations and 3 unknowns; with noisy data there is almost never a
solution that satisfies every equation at once (an inconsistent system).
Regression then looks not for an "exact solution" but for the one that
makes the **error smallest**: least squares. We will see it in the
Mathematics of Linear Regression section.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>Applying an operation only left of the bar</p>
      <p>Changing $R_1$ too in $R_2 - 2R_1$</p>
      <p>Trying to divide by a zero pivot</p>
      <p>Taking a $0 = 0$ row to mean "no solution"</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>To the whole row, right-hand side included</p>
      <p>Only $R_2$ changes, $R_1$ stays the same</p>
      <p>First swap with a lower row</p>
      <p>$0 = 0$ means infinitely many; $0 = c \ne 0$ means none</p>
    </div>
  </div>
  <figcaption>Elimination is mechanical work; most mistakes come from signs and forgetting the right-hand side.</figcaption>
</figure>

- **Sign errors.** $R_3 \to R_3 - (-2)R_2$ is the same as $R_3 + 2R_2$;
  write it once, then calculate.
- **Skipping the check.** Put your solution into the **original**
  equations; a mistake made during elimination is caught only this way.
- **Treating a free variable as a number.** In a system with infinitely
  many solutions, the answer is not a single point but a set depending on
  a parameter.

## Summary

- Linear system: $A\mathbf{x} = \mathbf{b}$; by hand use the augmented matrix $[A \mid \mathbf{b}]$.
- The number of solutions is always 0, 1 or infinitely many (lines: crossing, parallel, coinciding).
- Row operations: swap, scale by a non-zero number, add a multiple of another row.
- Forward elimination: clear below each pivot $\Rightarrow$ echelon form; then back substitution.
- A $0 = c \ne 0$ row: no solution. A column without a pivot: free variable, infinitely many solutions.
- Gauss–Jordan: $[A \mid I] \to [I \mid A^{-1}]$.
- $\det A$ = ($\pm$ by the number of swaps) product of the pivots.
- Computers: about $n^3/3$ operations, LU decomposition, partial pivoting.
- ML: finding parameters means solving a system; too little data $\Rightarrow$ infinitely many solutions, noisy data $\Rightarrow$ an inconsistent system and least squares.
