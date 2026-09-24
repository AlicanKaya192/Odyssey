# Determinants and Inverse Matrices

In the previous section we saw that a matrix is a **transformation**: it
rotates, stretches and reflects the plane. In this section we ask two
questions:

1. **By what factor** does a matrix change areas? The answer is a single
   number: the **determinant**.
2. **Can we undo** a transformation? The matrix that brings a transformed
   shape back to where it was is called the **inverse matrix**.

The two questions are linked: if the determinant is zero, the
transformation cannot be undone. That link also decides whether a system
of linear equations has a solution. In machine learning, the formula of
linear regression contains the inverse of a matrix, and the case where
that inverse does not exist is a common problem with real data.

Prerequisite: the Matrix Multiplication and Transformations section.

## The 2 × 2 determinant

The determinant of a square matrix is a single number computed from it.
It is written $\det A$ or $|A|$. For $2 \times 2$ the formula is:

$$
\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc
$$

**The product of the main diagonal minus the product of the other
diagonal.** Example:

$$
\det \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} = 3 \cdot 2 - 1 \cdot 1 = 5
$$

The determinant is defined only for **square** matrices. A $2 \times 3$
matrix has no determinant.

## What the determinant tells you: the area factor

Rather than memorising the formula, let us look at its meaning. In the
previous section we saw that the columns of a matrix are where
$\mathbf{e}_1$ and $\mathbf{e}_2$ go. So the unit square (area 1) turns
into the **parallelogram** spanned by these two columns.

<figure class="fig">
<svg viewBox="0 0 320 204" width="320"><line class="grid" x1="40" y1="192" x2="40" y2="16"/><line class="line" x1="84" y1="192" x2="84" y2="16"/><line class="grid" x1="128" y1="192" x2="128" y2="16"/><line class="grid" x1="172" y1="192" x2="172" y2="16"/><line class="grid" x1="216" y1="192" x2="216" y2="16"/><line class="grid" x1="260" y1="192" x2="260" y2="16"/><line class="grid" x1="40" y1="192" x2="260" y2="192"/><line class="line" x1="40" y1="148" x2="260" y2="148"/><line class="grid" x1="40" y1="104" x2="260" y2="104"/><line class="grid" x1="40" y1="60" x2="260" y2="60"/><line class="grid" x1="40" y1="16" x2="260" y2="16"/><text class="dim" x="40" y="161" font-size="9" text-anchor="middle">-1</text><text class="dim" x="128" y="161" font-size="9" text-anchor="middle">1</text><text class="dim" x="172" y="161" font-size="9" text-anchor="middle">2</text><text class="dim" x="216" y="161" font-size="9" text-anchor="middle">3</text><text class="dim" x="260" y="161" font-size="9" text-anchor="middle">4</text><text class="dim" x="79" y="195" font-size="9" text-anchor="end">-1</text><text class="dim" x="79" y="107" font-size="9" text-anchor="end">1</text><text class="dim" x="79" y="63" font-size="9" text-anchor="end">2</text><text class="dim" x="79" y="19" font-size="9" text-anchor="end">3</text><polygon class="dot" opacity="0.16" points="84,148 216,104 260,16 128,60"/><polygon class="curve3" points="84,148 216,104 260,16 128,60"/><polygon class="dot2" opacity="0.16" points="84,148 128,148 128,104 84,104"/><polygon class="curve3" stroke-dasharray="4 3" points="84,148 128,148 128,104 84,104"/><line class="curve" x1="84" y1="148" x2="209.2" y2="106.3"/><polygon class="dot" points="216,104 209.4,110.1 207.0,103.1"/><line class="curve2" x1="84" y1="148" x2="124.8" y2="66.4"/><polygon class="dot2" points="128,60 127.6,69.0 121.0,65.7"/><text class="ink" x="106.0" y="130.0" font-size="11" text-anchor="middle">area 1</text><text class="ink" x="176.4" y="71.0" font-size="13" text-anchor="middle">area |det A| = 5</text><text class="ink" x="222" y="116" font-size="11" text-anchor="start">(3, 1)</text><text class="ink" x="122" y="56" font-size="11" text-anchor="end">(1, 2)</text></svg>
  <figcaption>$A = \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix}$ takes the unit square (orange, area 1) to the parallelogram (purple) spanned by the columns $(3, 1)$ and $(1, 2)$. The parallelogram's area is $\det A = 5$.</figcaption>
</figure>

**The determinant tells you by what factor the matrix changes areas.** If
the unit square becomes a parallelogram of area 5, then **every** shape in
the plane grows 5 times in area: a triangle of area 2 becomes one of area
10. Every shape can be built from small squares, and every small square
grows by the same factor.

Let us check with familiar transformations:

| Matrix | Transformation | $\det$ | Meaning |
|---|---|---|---|
| $\begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$ | Scaling | $6$ | Width ×2, height ×3: area ×6 |
| $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ | $90°$ rotation | $1$ | A rotation does not change area |
| $\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ | Shear | $1$ | The square tilts but keeps its area |
| $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ | Projection | $0$ | The square is squashed into a segment |

It is interesting that a shear does not change area: the square becomes a
parallelogram, but its base and height stay the same. Area = base ×
height.

### The sign: did the orientation flip?

The determinant can also be **negative**. Its absolute value is still the
area factor; the minus sign says that the plane has been **flipped**
(turned into its mirror image).

<figure class="fig">
<svg viewBox="0 0 400 208" width="400"><line class="grid" x1="20" y1="176" x2="20" y2="16"/><line class="line" x1="60" y1="176" x2="60" y2="16"/><line class="grid" x1="100" y1="176" x2="100" y2="16"/><line class="grid" x1="140" y1="176" x2="140" y2="16"/><line class="grid" x1="180" y1="176" x2="180" y2="16"/><line class="grid" x1="20" y1="176" x2="180" y2="176"/><line class="line" x1="20" y1="136" x2="180" y2="136"/><line class="grid" x1="20" y1="96" x2="180" y2="96"/><line class="grid" x1="20" y1="56" x2="180" y2="56"/><line class="grid" x1="20" y1="16" x2="180" y2="16"/><polygon class="dot" opacity="0.16" points="60,136 100,136 100,96 60,96"/><polygon class="curve3" points="60,136 100,136 100,96 60,96"/><line class="curve" x1="60" y1="136" x2="92.8" y2="136.0"/><polygon class="dot" points="100,136 91.8,139.7 91.8,132.3"/><line class="curve2" x1="60" y1="136" x2="60.0" y2="103.2"/><polygon class="dot2" points="60,96 63.7,104.2 56.3,104.2"/><text class="ink" x="104" y="150" font-size="12" text-anchor="start">e₁</text><text class="ink" x="55" y="96" font-size="12" text-anchor="end">e₂</text><text class="ink" x="100.0" y="196" font-size="12" text-anchor="middle">Before: e₂ is left of e₁</text><line class="grid" x1="220" y1="176" x2="220" y2="16"/><line class="line" x1="260" y1="176" x2="260" y2="16"/><line class="grid" x1="300" y1="176" x2="300" y2="16"/><line class="grid" x1="340" y1="176" x2="340" y2="16"/><line class="grid" x1="380" y1="176" x2="380" y2="16"/><line class="grid" x1="220" y1="176" x2="380" y2="176"/><line class="line" x1="220" y1="136" x2="380" y2="136"/><line class="grid" x1="220" y1="96" x2="380" y2="96"/><line class="grid" x1="220" y1="56" x2="380" y2="56"/><line class="grid" x1="220" y1="16" x2="380" y2="16"/><polygon class="dot" opacity="0.16" points="260,136 300,56 380,16 340,96"/><polygon class="curve3" points="260,136 300,56 380,16 340,96"/><line class="curve" x1="260" y1="136" x2="296.8" y2="62.4"/><polygon class="dot" points="300,56 299.6,65.0 293.0,61.7"/><line class="curve2" x1="260" y1="136" x2="333.6" y2="99.2"/><polygon class="dot2" points="340,96 334.3,103.0 331.0,96.4"/><text class="ink" x="295" y="56" font-size="12" text-anchor="end">Be₁</text><text class="ink" x="345" y="108" font-size="12" text-anchor="start">Be₂</text><text class="ink" x="300.0" y="196" font-size="12" text-anchor="middle">After: flipped, det = −3</text></svg>
  <figcaption>On the left, $\mathbf{e}_2$ is to the left of $\mathbf{e}_1$ (anticlockwise from it). After $B = \begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}$ is applied, $B\mathbf{e}_2$ ends up to the right of $B\mathbf{e}_1$: the plane has been flipped. $\det B = 1 - 4 = -3$: area ×3, orientation reversed.</figcaption>
</figure>

That is why a reflection has determinant $-1$: same area, flipped
orientation.

$$
\det \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} = 1 \cdot (-1) - 0 \cdot 0 = -1
$$

### Zero determinant: the plane gets squashed

If $\det A = 0$, the unit square becomes a shape with **zero area**: a
line segment or a single point. This means the two columns lie **on the
same line**.

<figure class="fig">
<svg viewBox="0 0 310 200" width="310"><line class="grid" x1="30" y1="166" x2="30" y2="16"/><line class="line" x1="80" y1="166" x2="80" y2="16"/><line class="grid" x1="130" y1="166" x2="130" y2="16"/><line class="grid" x1="180" y1="166" x2="180" y2="16"/><line class="grid" x1="230" y1="166" x2="230" y2="16"/><line class="grid" x1="280" y1="166" x2="280" y2="16"/><line class="grid" x1="30" y1="166" x2="280" y2="166"/><line class="line" x1="30" y1="116" x2="280" y2="116"/><line class="grid" x1="30" y1="66" x2="280" y2="66"/><line class="grid" x1="30" y1="16" x2="280" y2="16"/><text class="dim" x="30" y="129" font-size="9" text-anchor="middle">-1</text><text class="dim" x="130" y="129" font-size="9" text-anchor="middle">1</text><text class="dim" x="180" y="129" font-size="9" text-anchor="middle">2</text><text class="dim" x="230" y="129" font-size="9" text-anchor="middle">3</text><text class="dim" x="280" y="129" font-size="9" text-anchor="middle">4</text><text class="dim" x="75" y="169" font-size="9" text-anchor="end">-1</text><text class="dim" x="75" y="69" font-size="9" text-anchor="end">1</text><text class="dim" x="75" y="19" font-size="9" text-anchor="end">2</text><polygon class="dot2" opacity="0.16" points="80,116 130,116 130,66 80,66"/><polygon class="curve3" stroke-dasharray="4 3" points="80,116 130,116 130,66 80,66"/><line class="curve3" stroke-dasharray="4 3" x1="30" y1="141.0" x2="280" y2="16"/><line class="curve4" x1="80" y1="116" x2="230" y2="41.0"/><line class="curve2" x1="80" y1="116" x2="173.6" y2="69.2"/><polygon class="dot2" points="180,66 174.3,73.0 171.0,66.4"/><line class="curve" x1="80" y1="116" x2="123.6" y2="94.2"/><polygon class="dot" points="130,91.0 124.3,98.0 121.0,91.4"/><circle class="dot3" cx="230" cy="41.0" r="3.5"/><text class="ink" x="155.0" y="188" font-size="12" text-anchor="middle">det = 0: the whole plane is squashed onto one line</text></svg>
  <figcaption>The columns of $\begin{bmatrix} 1 & 2 \\ 0.5 & 1 \end{bmatrix}$, $(1, 0.5)$ and $(2, 1)$, lie on the same line. The unit square is squashed into the green segment; the whole plane falls onto the dashed line.</figcaption>
</figure>

$$
\det \begin{bmatrix} 1 & 2 \\ 0.5 & 1 \end{bmatrix} = 1 \cdot 1 - 2 \cdot 0.5 = 0
$$

Information is **lost** here: every point of the plane lands on a single
line. Many different points go to the same place; for example $(2, 0)$
and $(0, 1)$ both go to $(2, 1)$. Looking at the result, the question
"which point did this come from?" can no longer be answered. As we will
see shortly, this matrix has no inverse.

A matrix with determinant zero is called **singular**.

## The 3 × 3 determinant

In three dimensions, the determinant tells you by what factor the matrix
changes the **volume** of the unit cube. The most common way to compute
it is to **expand along the first row**:

$$
\det \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
= a \begin{vmatrix} e & f \\ h & i \end{vmatrix}
- b \begin{vmatrix} d & f \\ g & i \end{vmatrix}
+ c \begin{vmatrix} d & e \\ g & h \end{vmatrix}
$$

Each first-row entry is multiplied by the determinant of the $2 \times 2$
matrix **left after deleting its own row and column**. The signs go $+,
-, +$. Example:

$$
A = \begin{bmatrix} 1 & 2 & 0 \\ 3 & 1 & 2 \\ 0 & 1 & 1 \end{bmatrix}
$$

$$
\begin{aligned}
\det A &= 1 \cdot (1 \cdot 1 - 2 \cdot 1) - 2 \cdot (3 \cdot 1 - 2 \cdot 0) + 0 \cdot (\dots) \\
&= 1 \cdot (-1) - 2 \cdot 3 + 0 \\
&= -7
\end{aligned}
$$

The term of a zero entry does not even need computing. That is why you
choose **the row or column with the most zeros** for the expansion (the
sign pattern is like a chessboard: $+ - +$, $- + -$, $+ - +$).

**The rule of Sarrus** (for $3 \times 3$ only): write the first two
columns once more on the right; add the products of the three diagonals
going down to the right, subtract the products of the three going down to
the left. For the same example:

$$
(1 \cdot 1 \cdot 1 + 2 \cdot 2 \cdot 0 + 0 \cdot 3 \cdot 1) - (0 \cdot 1 \cdot 0 + 1 \cdot 2 \cdot 1 + 2 \cdot 3 \cdot 1) = 1 - 8 = -7
$$

### The determinant of a triangular matrix

If everything below (or above) the diagonal is zero, the determinant is
**the product of the diagonal entries**:

$$
\det \begin{bmatrix} 2 & 5 & 1 \\ 0 & 3 & 4 \\ 0 & 0 & -1 \end{bmatrix} = 2 \cdot 3 \cdot (-1) = -6
$$

Expanding along the first column leaves a single term at each step.
Gaussian elimination in the next section computes the determinant of
large matrices exactly this way, by first bringing them to triangular
form.

## The rules of determinants

| Rule | Written as | Meaning |
|---|---|---|
| Product | $\det(AB) = \det A \cdot \det B$ | In a chain of transformations the area factors multiply |
| Transpose | $\det(A^\mathsf{T}) = \det A$ | Rows and columns are on equal terms |
| Identity | $\det I = 1$ | Nothing changes |
| Scalar | $\det(cA) = c^n \det A$ | In an $n \times n$ matrix every dimension grows $c$ times |
| Swapping rows | the sign flips | Swapping two rows reverses the orientation |
| Adding a row | unchanged | Adding a multiple of one row to another is a shear |
| Two equal rows | $\det = 0$ | The rows lie on the same line |

**The product rule** comes from geometry: if $B$ doubles areas and then
$A$ multiplies them by 5, the total is 10. Example:

$$
\det \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} = 5
\qquad
\det \begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix} = 2
$$

$$
\det \left( \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 0 & 2 \end{bmatrix} \right) = \det \begin{bmatrix} 3 & 5 \\ 1 & 5 \end{bmatrix} = 15 - 5 = 10
$$

**Careful with the scalar rule:** multiplying a $2 \times 2$ matrix by 2
doubles both directions, so area grows 4 times: $\det(2A) = 4 \det A$,
not $2 \det A$. For $3 \times 3$ it is $2^3 = 8$ times.

**There is no sum rule:** $\det(A + B) \ne \det A + \det B$ (in general).

## The inverse matrix

The inverse of a number is the number that gives 1 when multiplied by
it: $5 \cdot \tfrac{1}{5} = 1$. For matrices the counterpart of 1 is the
identity $I$. The **inverse** $A^{-1}$ of a square matrix $A$ is the
matrix that satisfies:

$$
A A^{-1} = A^{-1} A = I
$$

In the language of transformations: $A^{-1}$ is the transformation that
**undoes** what $A$ did. If $A$ moved a point, $A^{-1}$ brings it back:
$A^{-1}(A\mathbf{x}) = \mathbf{x}$.

### The 2 × 2 inverse formula

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix}^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}
$$

Three moves: **swap the two diagonal entries, flip the signs of the other
two, divide by the determinant.** Example:

$$
A = \begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix}
\qquad
\det A = 5
$$

$$
A^{-1} = \frac{1}{5} \begin{bmatrix} 2 & -1 \\ -1 & 3 \end{bmatrix} = \begin{bmatrix} 0.4 & -0.2 \\ -0.2 & 0.6 \end{bmatrix}
$$

**Always check:** is $AA^{-1}$ really $I$?

$$
\begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} 2 & -1 \\ -1 & 3 \end{bmatrix} = \begin{bmatrix} 6 - 1 & -3 + 3 \\ 2 - 2 & -1 + 6 \end{bmatrix} = \begin{bmatrix} 5 & 0 \\ 0 & 5 \end{bmatrix}
$$

Divided by $5$ this is $I$. ✓ (Leaving the division to the end saves you
from working with fractions.)

### When is there no inverse?

The formula divides by the determinant. **If $\det A = 0$, there is no
inverse.** We saw the geometric reason above: with determinant zero the
plane is squashed onto a line, many points go to the same place, and it
is impossible to know which came from where. No transformation can
un-squash something.

$$
A^{-1} \text{ exists} \iff \det A \ne 0
$$

A matrix that has an inverse is called **invertible** or **non-singular**.

### Inverses of transformations

Thinking geometrically, you can write most inverses without any
calculation:

| Transformation | Inverse |
|---|---|
| Rotation by $\theta$ | Rotation by $-\theta$ |
| Doubling $x$ | Halving $x$ |
| Shear by $k$ | Shear by $-k$ |
| Reflection | Itself (reflecting twice brings you back) |
| Projection | **None** (the height information is gone) |

### Rules of the inverse

| Rule | Written as |
|---|---|
| Inverse of the inverse | $(A^{-1})^{-1} = A$ |
| Inverse of a product | $(AB)^{-1} = B^{-1} A^{-1}$ |
| Inverse of the transpose | $(A^\mathsf{T})^{-1} = (A^{-1})^\mathsf{T}$ |
| Determinant | $\det(A^{-1}) = \dfrac{1}{\det A}$ |

**The inverse of a product reverses the order**, just like the transpose.
In the morning you put on socks and then shoes; in the evening you take
off the shoes first and then the socks. If $AB$ means "first $B$, then
$A$", undoing it means undoing $A$ first, then $B$: $B^{-1} A^{-1}$.

## Solving equations with the inverse

A system of equations can be written in matrix form:

$$
\begin{aligned}
3x + y &= 5 \\
x + 2y &= 5
\end{aligned}
\qquad \Longleftrightarrow \qquad
\begin{bmatrix} 3 & 1 \\ 1 & 2 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 5 \\ 5 \end{bmatrix}
$$

With numbers we solve $3x = 5$ by dividing both sides by 3. Matrices have
no division, but we can multiply both sides **on the left** by $A^{-1}$:

$$
A\mathbf{x} = \mathbf{b} \quad \Rightarrow \quad A^{-1} A \mathbf{x} = A^{-1}\mathbf{b} \quad \Rightarrow \quad \mathbf{x} = A^{-1}\mathbf{b}
$$

In our example we have already found $A^{-1}$:

$$
\mathbf{x} = \frac{1}{5} \begin{bmatrix} 2 & -1 \\ -1 & 3 \end{bmatrix} \begin{bmatrix} 5 \\ 5 \end{bmatrix} = \frac{1}{5} \begin{bmatrix} 5 \\ 10 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}
$$

Check: $3 \cdot 1 + 2 = 5$ and $1 + 2 \cdot 2 = 5$. ✓

**Multiplying on the left is essential.** Multiplying $A\mathbf{x}$ by
$A^{-1}$ on the right ($A\mathbf{x}A^{-1}$) is not even defined size-wise;
since matrix multiplication is not commutative, the side matters.

**Determinant and number of solutions.** If $\det A \ne 0$, the system
has **exactly one** solution: $\mathbf{x} = A^{-1}\mathbf{b}$. If $\det A
= 0$, there is either no solution or infinitely many; we will study these
cases with Gaussian elimination in the next section.

**In practice:** computers do not compute the inverse to solve large
systems; Gaussian elimination (next section) is both faster and more
robust against rounding errors. The inverse is used mostly **when writing
formulas**: $\mathbf{x} = A^{-1}\mathbf{b}$ is a short way of saying "this
is the solution".

## Determinants and inverses in machine learning

**The closed-form formula of linear regression.** For a data matrix $X$
and targets $\mathbf{y}$, the best weights are:

$$
\mathbf{w} = (X^\mathsf{T} X)^{-1} X^\mathsf{T} \mathbf{y}
$$

We will see where this formula comes from in the Mathematics of Linear
Regression section. For now what matters is this: it contains an
**inverse**, and if $X^\mathsf{T} X$ is singular the formula breaks down.

**The repeated-feature problem.** If one feature is a multiple of another
(square metres and "hundreds of square metres" as two columns of the same
table), the columns of $X$ lie on the same line and
$\det(X^\mathsf{T} X) = 0$. The model cannot separate the effects of the
two columns. This is called **multicollinearity**. With nearly identical
columns the determinant comes out very close to zero and the weights
become unstable and blow up to huge numbers.

**Ridge regularisation** fixes this by adding a small number to the
diagonal: $(X^\mathsf{T} X + \lambda I)^{-1}$. With $\lambda > 0$ the
matrix is always invertible.

**The multivariate normal distribution** (probability sections): its
formula contains the determinant and the inverse of the covariance
matrix. The determinant describes how "spread out" the data is (a
volume), and the inverse says in which directions distance counts more.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\det(A + B) = \det A + \det B$</p>
      <p>$\det(2A) = 2 \det A$ ($2 \times 2$)</p>
      <p>$(AB)^{-1} = A^{-1} B^{-1}$</p>
      <p>Inverse: the reciprocal of each entry $1/a_{ij}$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>No sum rule; $\det(AB) = \det A \det B$</p>
      <p>$\det(2A) = 4 \det A$</p>
      <p>$(AB)^{-1} = B^{-1} A^{-1}$</p>
      <p>$\frac{1}{ad - bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$</p>
    </div>
  </div>
  <figcaption>The determinant works with products, not sums. The inverse matrix is not the reciprocals of the entries.</figcaption>
</figure>

- **Mixing up positions in the inverse formula.** The diagonal $a$ and
  $d$ swap; $b$ and $c$ **stay where they are**, only their signs change.
- **Writing the inverse without computing the determinant.** Look at
  $\det$ first; if it is zero, there is no inverse, do not try the
  formula.
- **Forgetting the signs in a $3 \times 3$ expansion.** On the first row:
  $+, -, +$.
- **Skipping the check.** Multiply once to see whether $AA^{-1} = I$.

## Summary

- $\det \begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc$; square matrices only.
- $|\det A|$ is the area (in 3D, volume) factor; a minus sign says the orientation flipped.
- $\det A = 0$: the plane is squashed, information is lost, the matrix is singular.
- $3 \times 3$: expansion along the first row ($+, -, +$) or Sarrus; for triangular matrices, the product of the diagonal.
- $\det(AB) = \det A \det B$, $\det(A^\mathsf{T}) = \det A$, $\det(cA) = c^n \det A$.
- $A A^{-1} = I$; $2 \times 2$: swap, flip signs, divide by the determinant.
- An inverse exists $\iff$ $\det A \ne 0$. $(AB)^{-1} = B^{-1}A^{-1}$.
- If $A\mathbf{x} = \mathbf{b}$ then $\mathbf{x} = A^{-1}\mathbf{b}$ (multiply on the left).
- ML: $(X^\mathsf{T}X)^{-1}$; a repeated feature $\Rightarrow$ singular matrix; ridge adds $\lambda I$.
