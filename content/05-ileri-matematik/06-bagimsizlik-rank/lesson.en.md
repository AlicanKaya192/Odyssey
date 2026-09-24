# Linear Independence, Basis and Rank

Suppose a house data set has three columns: square metres, number of
rooms, and "area in hundreds of square metres". The third column says
nothing the first does not; it is just the first divided by 100. On paper
there are three features, but in reality there are **two** independent
pieces of information.

This section asks exactly this question in mathematical terms: how many
**genuinely different directions** are there in a group of vectors? The
answer is called the **rank**. Along the way we meet linear independence,
span, basis and dimension. They are the foundation of the eigenvalues,
SVD and PCA sections.

Prerequisite: the Linear Systems and Gaussian Elimination section.

## Linear combinations and span

Recall from the Vectors section: a **linear combination** of
$\mathbf{v}_1, \dots, \mathbf{v}_k$ multiplies them by numbers and adds
them up:

$$
c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + \cdots + c_k\mathbf{v}_k
$$

The set of all vectors reachable by giving the coefficients every
possible value is called the **span** of these vectors:
$\operatorname{span}(\mathbf{v}_1, \dots, \mathbf{v}_k)$.

- The span of a single non-zero vector is a **line** through the origin:
  every value of $c\,\mathbf{v}$.
- The span of two vectors pointing in different directions is a
  **plane**. If we are working in the plane, that means **the whole
  plane**.
- The span of two vectors in the same direction is still only a
  **line**. The second vector adds no new direction.

<figure class="fig">
<svg viewBox="0 0 420 210" width="420"><line class="grid" x1="20" y1="182" x2="20" y2="14"/><line class="grid" x1="48" y1="182" x2="48" y2="14"/><line class="grid" x1="76" y1="182" x2="76" y2="14"/><line class="line" x1="104" y1="182" x2="104" y2="14"/><line class="grid" x1="132" y1="182" x2="132" y2="14"/><line class="grid" x1="160" y1="182" x2="160" y2="14"/><line class="grid" x1="188" y1="182" x2="188" y2="14"/><line class="grid" x1="20" y1="182" x2="188" y2="182"/><line class="grid" x1="20" y1="154" x2="188" y2="154"/><line class="grid" x1="20" y1="126" x2="188" y2="126"/><line class="line" x1="20" y1="98" x2="188" y2="98"/><line class="grid" x1="20" y1="70" x2="188" y2="70"/><line class="grid" x1="20" y1="42" x2="188" y2="42"/><line class="grid" x1="20" y1="14" x2="188" y2="14"/><line class="curve4" x1="20.0" y1="182.0" x2="188.0" y2="14.0"/><line class="curve2" x1="104" y1="98" x2="154.9" y2="47.1"/><polygon class="dot2" points="160,42 156.8,50.4 151.6,45.2"/><line class="curve" x1="104" y1="98" x2="126.9" y2="75.1"/><polygon class="dot" points="132,70 128.8,78.4 123.6,73.2"/><text class="ink" x="138" y="80" font-size="12" text-anchor="start">v</text><text class="ink" x="166" y="46" font-size="12" text-anchor="start">w</text><text class="ink" x="104.0" y="200" font-size="11" text-anchor="middle">Dependent: w = 2v, only a line</text><line class="grid" x1="226" y1="182" x2="226" y2="14"/><line class="grid" x1="254" y1="182" x2="254" y2="14"/><line class="grid" x1="282" y1="182" x2="282" y2="14"/><line class="line" x1="310" y1="182" x2="310" y2="14"/><line class="grid" x1="338" y1="182" x2="338" y2="14"/><line class="grid" x1="366" y1="182" x2="366" y2="14"/><line class="grid" x1="394" y1="182" x2="394" y2="14"/><line class="grid" x1="226" y1="182" x2="394" y2="182"/><line class="grid" x1="226" y1="154" x2="394" y2="154"/><line class="grid" x1="226" y1="126" x2="394" y2="126"/><line class="line" x1="226" y1="98" x2="394" y2="98"/><line class="grid" x1="226" y1="70" x2="394" y2="70"/><line class="grid" x1="226" y1="42" x2="394" y2="42"/><line class="grid" x1="226" y1="14" x2="394" y2="14"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="310.0" y1="182.0" x2="394.0" y2="140.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="226.0" y1="182.0" x2="394.0" y2="98.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="310.0" y1="182.0" x2="226.0" y2="98.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="226.0" y1="140.0" x2="394.0" y2="56.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="394.0" y1="182.0" x2="226.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="226.0" y1="98.0" x2="394.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="394.0" y1="98.0" x2="310.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.7" x1="226.0" y1="56.0" x2="310.0" y2="14.0"/><line class="curve" x1="310" y1="98" x2="359.6" y2="73.2"/><polygon class="dot" points="366,70 360.3,77.0 357.0,70.4"/><line class="curve2" x1="310" y1="98" x2="287.1" y2="75.1"/><polygon class="dot2" points="282,70 290.4,73.2 285.2,78.4"/><line class="curve4" x1="310" y1="98" x2="334.8" y2="48.4"/><polygon class="dot3" points="338,42 337.6,51.0 331.0,47.7"/><text class="ink" x="372" y="74" font-size="12" text-anchor="start">v</text><text class="ink" x="276" y="74" font-size="12" text-anchor="end">w</text><text class="ink" x="344" y="42" font-size="11" text-anchor="start">v + w</text><text class="ink" x="310.0" y="200" font-size="11" text-anchor="middle">Independent: every point is a·v + b·w</text></svg>
  <figcaption>On the left $\mathbf{w} = 2\mathbf{v}$: every combination of the two stays on the green line. On the right $\mathbf{v} = (2, 1)$ and $\mathbf{w} = (-1, 1)$ point in different directions; every corner of the dashed grid is some $a\mathbf{v} + b\mathbf{w}$, and the grid covers the whole plane. The green arrow is $\mathbf{v} + \mathbf{w} = (1, 2)$.</figcaption>
</figure>

The span answers the question "where can I get with these vectors?". Its
link to matrices is direct: $A\mathbf{x}$ is a linear combination of the
columns of $A$ (the column view). So **all the values $A\mathbf{x}$ can
take form the span of the columns of $A$**. This is called the **column
space** of $A$.

## Linear dependence and independence

If one vector in a group is **a linear combination of the others**, the
group is **linearly dependent**: that vector adds no new direction, it is
redundant. If none is a combination of the others, the group is
**linearly independent**.

Example: $\mathbf{v}_1 = (1, 2, 1)$, $\mathbf{v}_2 = (2, 1, 0)$,
$\mathbf{v}_3 = (3, 3, 1)$. Looking closely, $\mathbf{v}_3 = \mathbf{v}_1 +
\mathbf{v}_2$: the group is dependent. There are three vectors, but what
they span is only a plane.

### The formal definition

The version of this definition written as an equation is more useful:
the vectors are independent if the **only** solution of

$$
c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + \cdots + c_k\mathbf{v}_k = \mathbf{0}
$$

is $c_1 = c_2 = \cdots = c_k = 0$. If there is a non-zero solution, they
are dependent.

Both definitions say the same thing: in our example $\mathbf{v}_1 +
\mathbf{v}_2 - \mathbf{v}_3 = \mathbf{0}$, so $c = (1, 1, -1)$ is a non-zero
solution. Solving it for $\mathbf{v}_3$ gives back $\mathbf{v}_3 =
\mathbf{v}_1 + \mathbf{v}_2$.

### How do we test independence?

**Two vectors:** if one is a multiple of the other they are dependent,
otherwise independent. $(2, 1)$ and $(4, 2)$ are dependent; $(2, 1)$ and
$(1, 2)$ are independent.

**The general way:** make the vectors the columns of a matrix and apply
Gaussian elimination.

$$
c_1\mathbf{v}_1 + \cdots + c_k\mathbf{v}_k = \mathbf{0}
\quad \Longleftrightarrow \quad
A\mathbf{c} = \mathbf{0}
$$

From the previous section: this system has only the solution $\mathbf{c}
= \mathbf{0}$ exactly when **every column has a pivot**. A column without
a pivot is a free variable, and a free variable means a non-zero
solution.

$$
\text{the columns are independent} \iff \text{every column has a pivot}
$$

**Square matrix:** for $n$ vectors in $n$ dimensions the quickest way is
the determinant. $\det A \ne 0$ means independent, $\det A = 0$ means
dependent. For $\mathbf{v}_1 = (1, 0, 1)$, $\mathbf{v}_2 = (0, 1, 1)$,
$\mathbf{v}_3 = (1, 1, 0)$:

$$
\det \begin{bmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \\ 1 & 1 & 0 \end{bmatrix} = 1 \cdot (0 - 1) - 0 + 1 \cdot (0 - 1) = -2 \ne 0
$$

These three are independent.

### Too many vectors are always dependent

In $n$-dimensional space, more than $n$ vectors are **always** dependent.
Take three vectors in the plane and one of them is bound to be a
combination of the others. Why? The matrix has $n$ rows, so there can be
at most $n$ pivots; with more than $n$ columns at least one has no pivot.

Any group containing the zero vector is dependent too: $1 \cdot \mathbf{0}
= \mathbf{0}$ is a non-zero solution.

## Basis and dimension

A **basis** of a space is a group of vectors that **spans** the space and
is **independent**. Both conditions matter:

- **It spans:** every vector of the space is a combination of these
  vectors. No direction is missing.
- **It is independent:** none of them is redundant. No extra direction.

The most familiar basis is the **standard basis**: $\mathbf{e}_1 = (1, 0)$
and $\mathbf{e}_2 = (0, 1)$. Every $(x, y) = x\,\mathbf{e}_1 +
y\,\mathbf{e}_2$.

But it is not the only one. In the plane, **any** two vectors pointing in
different directions form a basis. Every basis of a space has the same
number of vectors; that number is called the **dimension** of the space.
The plane is 2-dimensional, the space we live in is 3-dimensional, and an
image with 784 pixels lives in a 784-dimensional space.

### Coordinates in another basis

Once a basis is chosen, every vector can be written in terms of it in
**exactly one way**. The coefficients are the vector's **coordinates** in
that basis.

What are the coordinates of $(3, 1)$ in the basis $\mathbf{b}_1 = (1, 1)$,
$\mathbf{b}_2 = (1, -1)$? Write $c_1\mathbf{b}_1 + c_2\mathbf{b}_2 = (3,
1)$ component by component:

$$
\begin{aligned}
c_1 + c_2 &= 3 \\
c_1 - c_2 &= 1
\end{aligned}
$$

Adding gives $2c_1 = 4$, so $c_1 = 2$; then $c_2 = 1$.

<figure class="fig">
<svg viewBox="0 0 280 246" width="280"><line class="grid" x1="40" y1="214" x2="40" y2="14"/><line class="line" x1="80" y1="214" x2="80" y2="14"/><line class="grid" x1="120" y1="214" x2="120" y2="14"/><line class="grid" x1="160" y1="214" x2="160" y2="14"/><line class="grid" x1="200" y1="214" x2="200" y2="14"/><line class="grid" x1="240" y1="214" x2="240" y2="14"/><line class="grid" x1="40" y1="214" x2="240" y2="214"/><line class="grid" x1="40" y1="174" x2="240" y2="174"/><line class="line" x1="40" y1="134" x2="240" y2="134"/><line class="grid" x1="40" y1="94" x2="240" y2="94"/><line class="grid" x1="40" y1="54" x2="240" y2="54"/><line class="grid" x1="40" y1="14" x2="240" y2="14"/><text class="dim" x="40" y="147" font-size="9" text-anchor="middle">-1</text><text class="dim" x="120" y="147" font-size="9" text-anchor="middle">1</text><text class="dim" x="160" y="147" font-size="9" text-anchor="middle">2</text><text class="dim" x="200" y="147" font-size="9" text-anchor="middle">3</text><text class="dim" x="240" y="147" font-size="9" text-anchor="middle">4</text><text class="dim" x="75" y="217" font-size="9" text-anchor="end">-2</text><text class="dim" x="75" y="177" font-size="9" text-anchor="end">-1</text><text class="dim" x="75" y="97" font-size="9" text-anchor="end">1</text><text class="dim" x="75" y="57" font-size="9" text-anchor="end">2</text><text class="dim" x="75" y="17" font-size="9" text-anchor="end">3</text><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="94.0" x2="120.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="174.0" x2="80.0" y2="214.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="174.0" x2="200.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="94.0" x2="160.0" y2="214.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="80.0" y1="214.0" x2="240.0" y2="54.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="40.0" y1="14.0" x2="240.0" y2="214.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="160.0" y1="214.0" x2="240.0" y2="134.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="120.0" y1="14.0" x2="240.0" y2="134.0"/><line class="curve3" stroke-dasharray="4 3" opacity="0.55" x1="200.0" y1="14.0" x2="240.0" y2="54.0"/><line class="curve" x1="80" y1="134" x2="114.9" y2="99.1"/><polygon class="dot" points="120,94 116.8,102.4 111.6,97.2"/><line class="curve" x1="120" y1="94" x2="154.9" y2="59.1"/><polygon class="dot" points="160,54 156.8,62.4 151.6,57.2"/><line class="curve2" x1="160" y1="54" x2="194.9" y2="88.9"/><polygon class="dot2" points="200,94 191.6,90.8 196.8,85.6"/><line class="curve4" x1="80" y1="134" x2="193.2" y2="96.3"/><polygon class="dot3" points="200,94 193.4,100.1 191.0,93.1"/><text class="ink" x="94.0" y="112.0" font-size="12" text-anchor="end">b₁</text><text class="ink" x="186.0" y="72.0" font-size="12" text-anchor="start">b₂</text><text class="ink" x="206" y="106" font-size="11" text-anchor="start">(3, 1)</text><text class="ink" x="140.0" y="234" font-size="12" text-anchor="middle">(3, 1) = 2·b₁ + 1·b₂: new coordinates (2, 1)</text></svg>
  <figcaption>The dashed grid runs along $\mathbf{b}_1$ and $\mathbf{b}_2$. To reach $(3, 1)$, walking $\mathbf{b}_1$ twice (purple) and $\mathbf{b}_2$ once (orange) is enough. The same point is $(3, 1)$ in the standard basis and $(2, 1)$ in the new one.</figcaption>
</figure>

The point is the same; only the "rulers" we use to describe it changed.
**Changing coordinates** is one of the most powerful ideas of linear
algebra and machine learning: choosing the right basis makes a
complicated-looking problem simple. The eigenvalues and PCA sections ask
exactly the question "which basis is best?".

## Rank

The **rank** of a matrix is the number of its independent columns.
Equivalent definitions:

$$
\operatorname{rank} A = \text{number of independent columns} = \text{number of pivots} = \text{dimension of the column space}
$$

A surprising and important fact: **the number of independent rows is the
same number.** $\operatorname{rank} A = \operatorname{rank} A^\mathsf{T}$.
Elimination turns every row either into a pivot row or into a zero row;
the number of pivots tells the same story for rows and columns.

Example:

$$
A = \begin{bmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 1 & 1 & 1 \end{bmatrix}
$$

Row 2 is twice row 1; elimination shows it too. $R_2 - 2R_1$ and $R_3 -
R_1$:

$$
\begin{bmatrix} 1 & 2 & 3 \\ 0 & 0 & 0 \\ 0 & -1 & -2 \end{bmatrix}
\;\xrightarrow{R_2 \leftrightarrow R_3}\;
\begin{bmatrix} 1 & 2 & 3 \\ 0 & -1 & -2 \\ 0 & 0 & 0 \end{bmatrix}
$$

Two pivots: $\operatorname{rank} A = 2$. There are three columns but only
two are independent; three rows but only two are independent.

**Bounds:** for an $m \times n$ matrix, $\operatorname{rank} A \le
\min(m, n)$. If the rank equals this bound the matrix is called **full
rank**. A square matrix of full rank ($\operatorname{rank} = n$) is
invertible.

## The null space and the rank–nullity theorem

The set of all solutions of $A\mathbf{x} = \mathbf{0}$ is called the
**null space** (kernel) of $A$: the vectors $A$ sends to zero.
$\mathbf{x} = \mathbf{0}$ is always in it; the question is whether other
vectors are too.

For the $A$ above, from the echelon form:

$$
\begin{aligned}
x + 2y + 3z &= 0 \\
-y - 2z &= 0
\end{aligned}
$$

$z = t$ is free: $y = -2t$, $x = -2y - 3z = 4t - 3t = t$. The null space
is the line $t\,(1, -2, 1)$. Check: $A(1, -2, 1) = (1 - 4 + 3,\ 2 - 8 + 6,\ 1 - 2 + 1) = (0, 0, 0)$. ✓

The dimension of the null space is the number of free variables; the rank
is the number of pivots. Every column is either a pivot column or free,
so:

$$
\operatorname{rank} A + \dim(\text{null space}) = n \quad (\text{number of columns})
$$

This is the **rank–nullity theorem**. In our example $2 + 1 = 3$.

<figure class="fig">
<svg viewBox="0 0 420 210" width="420"><line class="grid" x1="20" y1="182" x2="20" y2="14"/><line class="grid" x1="48" y1="182" x2="48" y2="14"/><line class="grid" x1="76" y1="182" x2="76" y2="14"/><line class="line" x1="104" y1="182" x2="104" y2="14"/><line class="grid" x1="132" y1="182" x2="132" y2="14"/><line class="grid" x1="160" y1="182" x2="160" y2="14"/><line class="grid" x1="188" y1="182" x2="188" y2="14"/><line class="grid" x1="20" y1="182" x2="188" y2="182"/><line class="grid" x1="20" y1="154" x2="188" y2="154"/><line class="grid" x1="20" y1="126" x2="188" y2="126"/><line class="line" x1="20" y1="98" x2="188" y2="98"/><line class="grid" x1="20" y1="70" x2="188" y2="70"/><line class="grid" x1="20" y1="42" x2="188" y2="42"/><line class="grid" x1="20" y1="14" x2="188" y2="14"/><line class="curve2" x1="20.0" y1="56.0" x2="188.0" y2="140.0"/><circle class="dot2" cx="48" cy="70" r="3.5"/><circle class="dot2" cx="160" cy="126" r="3.5"/><text class="ink" x="156" y="144" font-size="11" text-anchor="end">(2, −1)</text><text class="ink" x="104.0" y="200" font-size="11" text-anchor="middle">Null space: points with Ax = 0</text><line class="grid" x1="226" y1="182" x2="226" y2="14"/><line class="grid" x1="254" y1="182" x2="254" y2="14"/><line class="grid" x1="282" y1="182" x2="282" y2="14"/><line class="line" x1="310" y1="182" x2="310" y2="14"/><line class="grid" x1="338" y1="182" x2="338" y2="14"/><line class="grid" x1="366" y1="182" x2="366" y2="14"/><line class="grid" x1="394" y1="182" x2="394" y2="14"/><line class="grid" x1="226" y1="182" x2="394" y2="182"/><line class="grid" x1="226" y1="154" x2="394" y2="154"/><line class="grid" x1="226" y1="126" x2="394" y2="126"/><line class="line" x1="226" y1="98" x2="394" y2="98"/><line class="grid" x1="226" y1="70" x2="394" y2="70"/><line class="grid" x1="226" y1="42" x2="394" y2="42"/><line class="grid" x1="226" y1="14" x2="394" y2="14"/><line class="curve" x1="268.0" y1="182.0" x2="352.0" y2="14.0"/><circle class="dot" cx="338" cy="42" r="3.5"/><circle class="dot" cx="282" cy="154" r="3.5"/><circle class="dot" cx="324.0" cy="70" r="3.5"/><text class="ink" x="330" y="38" font-size="11" text-anchor="end">A(1, 0) = (1, 2)</text><text class="ink" x="310.0" y="200" font-size="11" text-anchor="middle">Column space: all outputs</text></svg>
  <figcaption>For $A = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$ the rank is 1. Every point on the orange line on the left is sent to zero by $A$ (the null space, dimension 1). The purple line on the right holds every output $A$ can produce (the column space, dimension 1). $1 + 1 = 2$ columns.</figcaption>
</figure>

Geometrically: $A$ completely "wipes out" some directions (the null space)
and carries the remaining ones into the column space. The more directions
are wiped out, the smaller the column space.

## Rank and systems of equations

The three cases of the previous section can each be said in one sentence
with rank:

| Case | In terms of rank |
|---|---|
| A solution exists | $\operatorname{rank} A = \operatorname{rank}\,[A \mid \mathbf{b}]$ ($\mathbf{b}$ is in the column space) |
| No solution | $\operatorname{rank}\,[A \mid \mathbf{b}] > \operatorname{rank} A$ |
| Exactly one | a solution exists and $\operatorname{rank} A = n$ (null space is only $\mathbf{0}$) |
| Infinitely many | a solution exists and $\operatorname{rank} A < n$ |

When there are infinitely many, all solutions come from adding null-space
vectors to **one** solution: if $A\mathbf{x}_0 = \mathbf{b}$ and
$A\mathbf{n} = \mathbf{0}$, then $A(\mathbf{x}_0 + \mathbf{n}) =
\mathbf{b}$.

### The invertible matrix: six faces of one fact

For a square $n \times n$ matrix $A$, the following statements are **all
equivalent**; if one is true, they all are:

| | |
|---|---|
| 1 | $A$ is invertible |
| 2 | $\det A \ne 0$ |
| 3 | $\operatorname{rank} A = n$ |
| 4 | The columns are independent (so are the rows) |
| 5 | The null space is only $\mathbf{0}$ |
| 6 | $A\mathbf{x} = \mathbf{b}$ has exactly one solution for every $\mathbf{b}$ |

We met these one by one over the last three sections; now they turn out
to be different faces of the same fact.

## Rank in machine learning

**Repeated features.** In the house table from the start of the section,
one column is another divided by 100; the rank of the data matrix is less
than the number of columns. The singular $X^\mathsf{T}X$ we met in the
previous section is exactly this: if $X$ is not of full rank,
$X^\mathsf{T}X$ cannot be inverted. Adding a null-space vector to the
model's weights does not change the predictions at all, which is why the
weights are not unique.

**The real dimension.** A data set may have 1000 columns, yet its rank (or
approximate rank) may be far smaller: the data really sits in a
lower-dimensional subspace. Dimensionality reduction (PCA) finds this real
dimension and describes the data in that basis.

**Low-rank approximation.** On a film site, the user × film rating matrix
has millions of cells, yet tastes are made of a few basic tendencies
(liking action, liking romantic comedy, …). The matrix is approximately
low rank, and recommendation systems exploit that. In the SVD section we
will find the best low-rank approximation of a matrix.

**Embedding dimension.** Models that describe words or images with 300- or
768-dimensional vectors assume that meaning can be captured with that many
independent directions.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>Three vectors in the plane can be independent</p>
      <p>If none is a multiple of another, they are independent (3+ vectors)</p>
      <p>Rank = number of non-zero rows (before elimination)</p>
      <p>A basis is unique</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>At most $n$ independent vectors in $n$ dimensions</p>
      <p>One may be a <b>combination</b> of the others; eliminate</p>
      <p>Rank = number of pivots after elimination</p>
      <p>Every space has infinitely many bases, all the same size</p>
    </div>
  </div>
  <figcaption>Three vectors being pairwise "non-parallel" is not enough for independence: $(1, 2, 1)$, $(2, 1, 0)$ and their sum $(3, 3, 1)$ are pairwise non-parallel but dependent.</figcaption>
</figure>

- **Trying to read the rank without elimination.** A dependence may not be
  visible to the eye; counting pivots is the safest way.
- **Thinking row rank and column rank differ.** They are always equal.
- **Thinking the null space is empty.** The null space always contains
  $\mathbf{0}$; the question is whether it contains anything else.

## Summary

- Span: all combinations of the vectors. The span of $A$'s columns = column space = all values of $A\mathbf{x}$.
- Independence: the only solution of $c_1\mathbf{v}_1 + \cdots + c_k\mathbf{v}_k = \mathbf{0}$ is $\mathbf{c} = \mathbf{0}$. Test: a pivot in every column; if square, $\det \ne 0$.
- More than $n$ vectors in $n$ dimensions are always dependent.
- Basis: a group that spans and is independent. Dimension = number of vectors in a basis. Each vector has unique coordinates in a basis.
- Rank = number of independent columns = number of pivots = number of independent rows; $\le \min(m, n)$.
- Null space: the solutions of $A\mathbf{x} = \mathbf{0}$. $\operatorname{rank} A + \dim(\text{null space}) = n$.
- Square $A$: invertible $\iff \det \ne 0 \iff$ rank $n$ $\iff$ independent columns $\iff$ null space $\{\mathbf{0}\}$.
- ML: repeated feature $\Rightarrow$ low rank, non-unique weights; the real dimension of data; low-rank approximation.
