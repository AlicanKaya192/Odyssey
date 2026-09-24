# Matrix Multiplication and Transformations

In the previous section we multiplied a matrix by a vector: the product of
the house table $X$ and the weight vector $\mathbf{w}$ gave the price
predictions for every house at once. Now let us go one step further.
Suppose we have **two different models**: one predicts the price, the other
the rental yield. Putting the two weight vectors side by side gives a
matrix, and the question becomes: **how do we multiply a matrix by another
matrix?**

Matrix multiplication is the most used operation in linear algebra. Every
layer of a neural network, rotating a photo, transforming every row of a
data table at once; all of them are matrix multiplication. In this section
we will see:

- How two matrices are multiplied and the size rule,
- Why the product **depends on the order**,
- How a matrix **rotates, stretches and reflects** the plane,
- Why doing two transformations one after another is a matrix product.

Prerequisite: the Matrices section (especially the matrix–vector product).

## The size rule

Two matrices can be multiplied only when **the number of columns of the
left one equals the number of rows of the right one**. The result has as
many rows as the left one and as many columns as the right one:

$$
\underbrace{A}_{m \times n}\;\underbrace{B}_{n \times p} = \underbrace{C}_{m \times p}
$$

Writing the sizes next to each other makes the rule readable at a glance:
$(m \times \boxed{n})(\boxed{n} \times p)$. **The two inner numbers must
match, the two outer numbers give the size of the result.**

| $A$ | $B$ | $AB$ |
|---|---|---|
| $2 \times 3$ | $3 \times 4$ | $2 \times 4$ |
| $3 \times 3$ | $3 \times 1$ | $3 \times 1$ (matrix–vector product) |
| $1 \times 3$ | $3 \times 1$ | $1 \times 1$ (a single number: the dot product) |
| $3 \times 1$ | $1 \times 3$ | $3 \times 3$ |
| $2 \times 3$ | $2 \times 3$ | undefined ($3 \ne 2$) |

Look at the second and third rows of the table: the matrix–vector product
and the dot product we met earlier are **special cases** of matrix
multiplication. We are not learning a new operation, we are extending one
we already know.

## The entry rule: row times column

The entry in row $i$, column $j$ of $C = AB$ is **the dot product of row
$i$ of $A$ with column $j$ of $B$**:

$$
c_{ij} = a_{i1} b_{1j} + a_{i2} b_{2j} + \cdots + a_{in} b_{nj}
$$

This is also the reason for the size rule: to take a dot product, the
length of a row of $A$ ($n$) must equal the length of a column of $B$
($n$).

<figure class="fig">
<svg viewBox="0 0 400 228" width="400"><rect class="box" x="20" y="70" width="34" height="34"/><text class="ink" x="37.0" y="92.0" font-size="14" text-anchor="middle">1</text><rect class="box" x="54" y="70" width="34" height="34"/><text class="ink" x="71.0" y="92.0" font-size="14" text-anchor="middle">2</text><rect class="box" x="88" y="70" width="34" height="34"/><text class="ink" x="105.0" y="92.0" font-size="14" text-anchor="middle">3</text><rect class="box" x="20" y="104" width="34" height="34"/><text class="ink" x="37.0" y="126.0" font-size="14" text-anchor="middle">4</text><rect class="box" x="54" y="104" width="34" height="34"/><text class="ink" x="71.0" y="126.0" font-size="14" text-anchor="middle">5</text><rect class="box" x="88" y="104" width="34" height="34"/><text class="ink" x="105.0" y="126.0" font-size="14" text-anchor="middle">6</text><rect class="box" x="162" y="53" width="34" height="34"/><text class="ink" x="179.0" y="75.0" font-size="14" text-anchor="middle">1</text><rect class="box" x="196" y="53" width="34" height="34"/><text class="ink" x="213.0" y="75.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="162" y="87" width="34" height="34"/><text class="ink" x="179.0" y="109.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="196" y="87" width="34" height="34"/><text class="ink" x="213.0" y="109.0" font-size="14" text-anchor="middle">1</text><rect class="box" x="162" y="121" width="34" height="34"/><text class="ink" x="179.0" y="143.0" font-size="14" text-anchor="middle">2</text><rect class="box" x="196" y="121" width="34" height="34"/><text class="ink" x="213.0" y="143.0" font-size="14" text-anchor="middle">1</text><rect class="box" x="270" y="70" width="34" height="34"/><text class="ink" x="287.0" y="92.0" font-size="14" text-anchor="middle">7</text><rect class="box" x="304" y="70" width="34" height="34"/><text class="ink" x="321.0" y="92.0" font-size="14" text-anchor="middle">5</text><rect class="box" x="270" y="104" width="34" height="34"/><text class="ink" x="287.0" y="126.0" font-size="14" text-anchor="middle">16</text><rect class="box" x="304" y="104" width="34" height="34"/><text class="ink" x="321.0" y="126.0" font-size="14" text-anchor="middle">11</text><rect class="curve" x="17" y="67" width="108" height="40" rx="4"/><rect class="curve2" x="193" y="50" width="40" height="108" rx="4"/><rect class="curve4" x="301" y="67" width="40" height="40" rx="4"/><text class="ink" x="71.0" y="56" font-size="12" text-anchor="middle">A  (2 × 3)</text><text class="ink" x="196" y="39" font-size="12" text-anchor="middle">B  (3 × 2)</text><text class="ink" x="304" y="56" font-size="12" text-anchor="middle">AB  (2 × 2)</text><text class="ink" x="142" y="109" font-size="20" text-anchor="middle">·</text><text class="ink" x="250" y="109" font-size="18" text-anchor="middle">=</text><text class="ink" x="71.0" y="160" font-size="12" text-anchor="middle">row 1</text><text class="ink" x="213.0" y="175" font-size="12" text-anchor="middle">column 2</text><text class="ink" x="200" y="212" font-size="14" text-anchor="middle">c₁₂ = 1 · 0 + 2 · 1 + 3 · 1 = 5</text></svg>
  <figcaption>Multiplying row 1 of $A$ (purple) by column 2 of $B$ (orange) and adding gives the entry of $AB$ in row 1, column 2 (green).</figcaption>
</figure>

Let us compute every entry in an example:

$$
A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}
\qquad
B = \begin{bmatrix} 1 & 4 \\ 2 & -1 \end{bmatrix}
$$

For each entry we pick one row and one column:

$$
\begin{aligned}
c_{11} &= (2, 1) \cdot (1, 2) = 2 + 2 = 4 \\
c_{12} &= (2, 1) \cdot (4, -1) = 8 - 1 = 7 \\
c_{21} &= (0, 3) \cdot (1, 2) = 0 + 6 = 6 \\
c_{22} &= (0, 3) \cdot (4, -1) = 0 - 3 = -3
\end{aligned}
$$

$$
AB = \begin{bmatrix} 4 & 7 \\ 6 & -3 \end{bmatrix}
$$

**A practical routine:** to compute $c_{ij}$, run a finger of your left
hand along row $i$ of $A$ from left to right and a finger of your right
hand down column $j$ of $B$; multiply the numbers the fingers stop on and
add.

## The column view: each column of B is a separate matrix–vector product

If we split $B$ into its columns, each column of $AB$ is $A$ times that
column of $B$:

$$
AB = A \begin{bmatrix} \mathbf{b}_1 & \mathbf{b}_2 \end{bmatrix} = \begin{bmatrix} A\mathbf{b}_1 & A\mathbf{b}_2 \end{bmatrix}
$$

In the example above:

$$
A\mathbf{b}_1 = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 4 \\ 6 \end{bmatrix}
$$

That is column 1 of $AB$. Matrix multiplication means **applying the same
$A$ to many vectors at once**. Multiplying every row of a data matrix by
the same weights, or rotating every point of a photo the same way, is
exactly this.

## The product depends on the order

With numbers, $3 \cdot 5 = 5 \cdot 3$. With matrices this is **usually not
true**. Let us compute $BA$ for the same $A$ and $B$:

$$
BA = \begin{bmatrix} 1 & 4 \\ 2 & -1 \end{bmatrix} \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} = \begin{bmatrix} 2 & 13 \\ 4 & -1 \end{bmatrix}
$$

$AB$ was $\begin{bmatrix} 4 & 7 \\ 6 & -3 \end{bmatrix}$. They differ:
$AB \ne BA$. Sometimes one is even defined while the other is not: if $A$
is $2 \times 3$ and $B$ is $3 \times 4$, then $AB$ exists ($2 \times 4$)
but $BA$ does not ($4 \ne 2$).

So in matrix multiplication "multiplying on the left" and "multiplying on
the right" are different things. When you multiply both sides of an
equation by a matrix, you have to multiply **from the same side**.

**Why?** As we will see shortly, a matrix is a **transformation** and the
product performs two transformations one after the other. Putting on
socks and then shoes is not the same as shoes and then socks; with
transformations, order matters too.

## The rules of multiplication

Apart from order, most rules of numbers still hold:

| Rule | Written as |
|---|---|
| Associativity | $(AB)C = A(BC)$ |
| Left distributivity | $A(B + C) = AB + AC$ |
| Right distributivity | $(A + B)C = AC + BC$ |
| Scalars | $(cA)B = c(AB) = A(cB)$ |
| Identity | $AI = IA = A$ |
| Transpose | $(AB)^\mathsf{T} = B^\mathsf{T} A^\mathsf{T}$ |
| Commutativity | **generally no:** $AB \ne BA$ |

**Associativity** is very useful: $(AB)C$ and $A(BC)$ are the same, so you
may put the brackets wherever you like (but you may not change the order).
To do three transformations in a row, it does not matter which two you
combine first.

**The transpose rule reverses the order:** $(AB)^\mathsf{T} =
B^\mathsf{T} A^\mathsf{T}$, not $A^\mathsf{T} B^\mathsf{T}$. In our
example:

$$
(AB)^\mathsf{T} = \begin{bmatrix} 4 & 6 \\ 7 & -3 \end{bmatrix}
= \begin{bmatrix} 1 & 2 \\ 4 & -1 \end{bmatrix} \begin{bmatrix} 2 & 0 \\ 1 & 3 \end{bmatrix}
= B^\mathsf{T} A^\mathsf{T}
$$

The sizes agree too: if $A$ is $2 \times 3$ and $B$ is $3 \times 4$, then
$(AB)^\mathsf{T}$ is $4 \times 2$; $B^\mathsf{T}$ ($4 \times 3$) times
$A^\mathsf{T}$ ($3 \times 2$) is also $4 \times 2$. The other order cannot
even be multiplied.

### Powers

A square matrix can be multiplied by itself: $A^2 = AA$, $A^3 = AAA$.

$$
A^2 = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix} = \begin{bmatrix} 4 & 5 \\ 0 & 9 \end{bmatrix}
$$

**Careful:** $A^2$ is **not** squaring the entries. Squaring the entries
would give $\begin{bmatrix} 4 & 1 \\ 0 & 9 \end{bmatrix}$; the top-right
$5$ and $1$ differ.

## A matrix is a transformation

Now the second, and perhaps most important, idea of the section.
Multiplying a $2 \times 2$ matrix by a vector gives a new vector. So a
matrix is a rule that **takes** every point of the plane to another point:
a **transformation**.

### The columns tell you everything

The quick way to understand what a matrix does is to see where the two
standard unit vectors go: $\mathbf{e}_1 = (1, 0)$ and $\mathbf{e}_2 = (0, 1)$.

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} a \\ c \end{bmatrix}
\qquad
\begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} 0 \\ 1 \end{bmatrix} = \begin{bmatrix} b \\ d \end{bmatrix}
$$

**$\mathbf{e}_1$ goes to the 1st column of the matrix, $\mathbf{e}_2$ to
the 2nd.** Every other vector is built from $\mathbf{e}_1$ and
$\mathbf{e}_2$ ($(x, y) = x\,\mathbf{e}_1 + y\,\mathbf{e}_2$), so knowing
where they go means knowing where everything goes. This is the geometric
meaning of the column view of the matrix–vector product.

It also works the other way round: if you say "I want to transform the
plane like this", you write its matrix by placing the desired images of
$\mathbf{e}_1$ and $\mathbf{e}_2$ side by side as columns.

### Four basic transformations

<figure class="fig">
<svg viewBox="0 0 400 444" width="400"><line class="grid" x1="26" y1="152" x2="26" y2="16"/><line class="grid" x1="60" y1="152" x2="60" y2="16"/><line class="line" x1="94" y1="152" x2="94" y2="16"/><line class="grid" x1="128" y1="152" x2="128" y2="16"/><line class="grid" x1="162" y1="152" x2="162" y2="16"/><line class="grid" x1="26" y1="152" x2="162" y2="152"/><line class="grid" x1="26" y1="118" x2="162" y2="118"/><line class="line" x1="26" y1="84" x2="162" y2="84"/><line class="grid" x1="26" y1="50" x2="162" y2="50"/><line class="grid" x1="26" y1="16" x2="162" y2="16"/><polygon class="curve3" stroke-dasharray="4 3" points="94,84 128,84 128,50 94,50"/><polygon class="dot" opacity="0.16" points="94,84 162,84 162,50 94,50"/><polygon class="curve3" points="94,84 162,84 162,50 94,50"/><line class="curve" x1="94" y1="84" x2="154.8" y2="84.0"/><polygon class="dot" points="162,84 153.8,87.7 153.8,80.3"/><line class="curve2" x1="94" y1="84" x2="94.0" y2="57.2"/><polygon class="dot2" points="94,50 97.7,58.2 90.3,58.2"/><text class="ink" x="94.0" y="170" font-size="12" text-anchor="middle">Scaling</text><text class="dim" x="94.0" y="185" font-size="11" text-anchor="middle">[2 0; 0 1]</text><line class="grid" x1="222" y1="152" x2="222" y2="16"/><line class="grid" x1="256" y1="152" x2="256" y2="16"/><line class="line" x1="290" y1="152" x2="290" y2="16"/><line class="grid" x1="324" y1="152" x2="324" y2="16"/><line class="grid" x1="358" y1="152" x2="358" y2="16"/><line class="grid" x1="222" y1="152" x2="358" y2="152"/><line class="grid" x1="222" y1="118" x2="358" y2="118"/><line class="line" x1="222" y1="84" x2="358" y2="84"/><line class="grid" x1="222" y1="50" x2="358" y2="50"/><line class="grid" x1="222" y1="16" x2="358" y2="16"/><polygon class="curve3" stroke-dasharray="4 3" points="290,84 324,84 324,50 290,50"/><polygon class="dot" opacity="0.16" points="290,84 290,50 256,50 256,84"/><polygon class="curve3" points="290,84 290,50 256,50 256,84"/><line class="curve" x1="290" y1="84" x2="290.0" y2="57.2"/><polygon class="dot" points="290,50 293.7,58.2 286.3,58.2"/><line class="curve2" x1="290" y1="84" x2="263.2" y2="84.0"/><polygon class="dot2" points="256,84 264.2,80.3 264.2,87.7"/><text class="ink" x="290.0" y="170" font-size="12" text-anchor="middle">90° rotation</text><text class="dim" x="290.0" y="185" font-size="11" text-anchor="middle">[0 −1; 1 0]</text><line class="grid" x1="26" y1="366" x2="26" y2="230"/><line class="grid" x1="60" y1="366" x2="60" y2="230"/><line class="line" x1="94" y1="366" x2="94" y2="230"/><line class="grid" x1="128" y1="366" x2="128" y2="230"/><line class="grid" x1="162" y1="366" x2="162" y2="230"/><line class="grid" x1="26" y1="366" x2="162" y2="366"/><line class="grid" x1="26" y1="332" x2="162" y2="332"/><line class="line" x1="26" y1="298" x2="162" y2="298"/><line class="grid" x1="26" y1="264" x2="162" y2="264"/><line class="grid" x1="26" y1="230" x2="162" y2="230"/><polygon class="curve3" stroke-dasharray="4 3" points="94,298 128,298 128,264 94,264"/><polygon class="dot" opacity="0.16" points="94,298 128,298 128,332 94,332"/><polygon class="curve3" points="94,298 128,298 128,332 94,332"/><line class="curve" x1="94" y1="298" x2="120.8" y2="298.0"/><polygon class="dot" points="128,298 119.8,301.7 119.8,294.3"/><line class="curve2" x1="94" y1="298" x2="94.0" y2="324.8"/><polygon class="dot2" points="94,332 90.3,323.8 97.7,323.8"/><text class="ink" x="94.0" y="384" font-size="12" text-anchor="middle">Reflection in x-axis</text><text class="dim" x="94.0" y="399" font-size="11" text-anchor="middle">[1 0; 0 −1]</text><line class="grid" x1="222" y1="366" x2="222" y2="230"/><line class="grid" x1="256" y1="366" x2="256" y2="230"/><line class="line" x1="290" y1="366" x2="290" y2="230"/><line class="grid" x1="324" y1="366" x2="324" y2="230"/><line class="grid" x1="358" y1="366" x2="358" y2="230"/><line class="grid" x1="222" y1="366" x2="358" y2="366"/><line class="grid" x1="222" y1="332" x2="358" y2="332"/><line class="line" x1="222" y1="298" x2="358" y2="298"/><line class="grid" x1="222" y1="264" x2="358" y2="264"/><line class="grid" x1="222" y1="230" x2="358" y2="230"/><polygon class="curve3" stroke-dasharray="4 3" points="290,298 324,298 324,264 290,264"/><polygon class="dot" opacity="0.16" points="290,298 324,298 358,264 324,264"/><polygon class="curve3" points="290,298 324,298 358,264 324,264"/><line class="curve" x1="290" y1="298" x2="316.8" y2="298.0"/><polygon class="dot" points="324,298 315.8,301.7 315.8,294.3"/><line class="curve2" x1="290" y1="298" x2="318.9" y2="269.1"/><polygon class="dot2" points="324,264 320.8,272.4 315.6,267.2"/><text class="ink" x="290.0" y="384" font-size="12" text-anchor="middle">Shear</text><text class="dim" x="290.0" y="399" font-size="11" text-anchor="middle">[1 1; 0 1]</text></svg>
  <figcaption>The dashed square is the unit square before the transformation, the filled shape is after it. The purple arrow is where $\mathbf{e}_1$ goes, the orange arrow where $\mathbf{e}_2$ goes: the 1st and 2nd columns of the matrix.</figcaption>
</figure>

| Transformation | Matrix | What it does |
|---|---|---|
| Scaling | $\begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}$ | Doubles $x$, leaves $y$ alone |
| 90° rotation | $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ | Turns everything 90° anticlockwise |
| Reflection | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ | Mirror in the $x$-axis: $(x, y) \to (x, -y)$ |
| Shear | $\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$ | Slides higher points to the right: $(x, y) \to (x + y, y)$ |
| Projection | $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ | Drops every point onto the $x$-axis: $(x, y) \to (x, 0)$ |

Let us check the rotation with an example. Rotate the point $(3, 1)$ by
90°:

$$
\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 3 \\ 1 \end{bmatrix} = \begin{bmatrix} 0 \cdot 3 + (-1) \cdot 1 \\ 1 \cdot 3 + 0 \cdot 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 3 \end{bmatrix}
$$

$(3, 1)$ was to the right and a little up; $(-1, 3)$ is up and a little to
the left: it really turned a quarter. The length did not change either:
$\sqrt{9 + 1} = \sqrt{1 + 9}$.

### Rotation by any angle

Rotation anticlockwise by an angle $\theta$:

$$
R_\theta = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}
$$

Read it with the column rule: $\mathbf{e}_1 = (1, 0)$, turned by $\theta$
on the unit circle, lands on $(\cos\theta, \sin\theta)$ (1st column).
$\mathbf{e}_2$ is $90°$ ahead of it, at $(-\sin\theta, \cos\theta)$ (2nd
column). Putting $\theta = 90°$ gives $\cos 90° = 0$, $\sin 90° = 1$ and
the matrix above.

### What does linear transformation mean?

Every transformation done by a matrix has two properties (the rules from
the Matrices section):

$$
A(\mathbf{x} + \mathbf{y}) = A\mathbf{x} + A\mathbf{y}
\qquad
A(c\,\mathbf{x}) = c\,A\mathbf{x}
$$

The geometric meaning: **the origin stays put, lines stay lines, parallel
lines stay parallel and grid lines stay evenly spaced.** A square may
become a parallelogram but never a curve. Transformations with these
properties are called **linear transformations**, and every linear
transformation can be written as a matrix.

A translation (shifting every point by $(1, 0)$) is **not** linear in this
sense: it moves the origin, so it cannot be written as a single
$2 \times 2$ matrix.

## Two transformations in a row = matrix multiplication

Apply first $B$, then $A$ to a vector:

$$
A(B\mathbf{x}) = (AB)\mathbf{x}
$$

This equality comes from associativity and says a lot: **doing two
transformations one after the other is the same as doing the single
transformation given by their product.** Instead of rotating a thousand
points and then scaling them, you can multiply the two matrices once and
apply the single matrix to the thousand points.

**Read from right to left.** In $AB\mathbf{x}$ the matrix nearest the
vector ($B$) is applied first. $AB$ means "first $B$, then $A$". It is the
same as $g$ being applied first in $f(g(x))$.

### Why order matters: an example

Let $R$ be the 90° rotation and $S$ the reflection in the $x$-axis. Apply
both to $\mathbf{v} = (2, 1)$ in two different orders.

<figure class="fig">
<svg viewBox="0 0 420 212" width="420"><line class="grid" x1="30" y1="176" x2="30" y2="16"/><line class="grid" x1="70" y1="176" x2="70" y2="16"/><line class="line" x1="110" y1="176" x2="110" y2="16"/><line class="grid" x1="150" y1="176" x2="150" y2="16"/><line class="grid" x1="190" y1="176" x2="190" y2="16"/><line class="grid" x1="30" y1="176" x2="190" y2="176"/><line class="grid" x1="30" y1="136" x2="190" y2="136"/><line class="line" x1="30" y1="96" x2="190" y2="96"/><line class="grid" x1="30" y1="56" x2="190" y2="56"/><line class="grid" x1="30" y1="16" x2="190" y2="16"/><text class="dim" x="30" y="109" font-size="9" text-anchor="middle">-2</text><text class="dim" x="70" y="109" font-size="9" text-anchor="middle">-1</text><text class="dim" x="150" y="109" font-size="9" text-anchor="middle">1</text><text class="dim" x="190" y="109" font-size="9" text-anchor="middle">2</text><text class="dim" x="105" y="179" font-size="9" text-anchor="end">-2</text><text class="dim" x="105" y="139" font-size="9" text-anchor="end">-1</text><text class="dim" x="105" y="59" font-size="9" text-anchor="end">1</text><text class="dim" x="105" y="19" font-size="9" text-anchor="end">2</text><line class="curve4" x1="110" y1="96" x2="183.6" y2="59.2"/><polygon class="dot3" points="190,56 184.3,63.0 181.0,56.4"/><line class="curve3" stroke-dasharray="4 3" x1="110" y1="96" x2="73.2" y2="22.4"/><polygon class="dim" points="70,16 77.0,21.7 70.4,25.0"/><line class="curve" x1="110" y1="96" x2="73.2" y2="169.6"/><polygon class="dot" points="70,176 70.4,167.0 77.0,170.3"/><text class="ink" x="195" y="52" font-size="12" text-anchor="start">v</text><text class="ink" x="63" y="180" font-size="11" text-anchor="end">(-1, -2)</text><text class="ink" x="110.0" y="200" font-size="12" text-anchor="middle">Rotate, then reflect: SRv</text><line class="grid" x1="240" y1="176" x2="240" y2="16"/><line class="grid" x1="280" y1="176" x2="280" y2="16"/><line class="line" x1="320" y1="176" x2="320" y2="16"/><line class="grid" x1="360" y1="176" x2="360" y2="16"/><line class="grid" x1="400" y1="176" x2="400" y2="16"/><line class="grid" x1="240" y1="176" x2="400" y2="176"/><line class="grid" x1="240" y1="136" x2="400" y2="136"/><line class="line" x1="240" y1="96" x2="400" y2="96"/><line class="grid" x1="240" y1="56" x2="400" y2="56"/><line class="grid" x1="240" y1="16" x2="400" y2="16"/><text class="dim" x="240" y="109" font-size="9" text-anchor="middle">-2</text><text class="dim" x="280" y="109" font-size="9" text-anchor="middle">-1</text><text class="dim" x="360" y="109" font-size="9" text-anchor="middle">1</text><text class="dim" x="400" y="109" font-size="9" text-anchor="middle">2</text><text class="dim" x="315" y="179" font-size="9" text-anchor="end">-2</text><text class="dim" x="315" y="139" font-size="9" text-anchor="end">-1</text><text class="dim" x="315" y="59" font-size="9" text-anchor="end">1</text><text class="dim" x="315" y="19" font-size="9" text-anchor="end">2</text><line class="curve4" x1="320" y1="96" x2="393.6" y2="59.2"/><polygon class="dot3" points="400,56 394.3,63.0 391.0,56.4"/><line class="curve3" stroke-dasharray="4 3" x1="320" y1="96" x2="393.6" y2="132.8"/><polygon class="dim" points="400,136 391.0,135.6 394.3,129.0"/><line class="curve2" x1="320" y1="96" x2="356.8" y2="22.4"/><polygon class="dot2" points="360,16 359.6,25.0 353.0,21.7"/><text class="ink" x="405" y="52" font-size="12" text-anchor="start">v</text><text class="ink" x="367" y="20" font-size="11" text-anchor="start">(1, 2)</text><text class="ink" x="320.0" y="200" font-size="12" text-anchor="middle">Reflect, then rotate: RSv</text></svg>
  <figcaption>The green arrow is $\mathbf{v} = (2, 1)$, the dashed arrow the state after the first transformation. The same two transformations land in different places when the order changes.</figcaption>
</figure>

**Rotate, then reflect** ($SR\mathbf{v}$): rotating gives $(-1, 2)$,
reflecting then gives $(-1, -2)$.

**Reflect, then rotate** ($RS\mathbf{v}$): reflecting gives $(2, -1)$,
rotating then gives $(1, 2)$.

The results differ. We can see it by multiplying the matrices too:

$$
SR = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & -1 \\ -1 & 0 \end{bmatrix}
$$

$$
RS = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix} = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
$$

$SR \ne RS$. This is the geometric face of "matrix multiplication is not
commutative".

### Some transformations do not mind the order

Two rotations in a row are a single rotation by the sum of the angles:
$R_\alpha R_\beta = R_{\alpha + \beta} = R_\beta R_\alpha$. Two scalings
do not mind the order either. But these are exceptions; as a general rule,
assume order matters.

## Matrix multiplication in machine learning

**Every row of a data matrix, every model.** Let $X$ be an $n \times d$
data matrix (row = example) and $W$ a $d \times k$ weight matrix (column =
one model). $XW$ is $n \times k$: the predictions of $k$ models for every
example, in one product. The generalisation of what we did with a single
$\mathbf{w}$ in the previous section.

**Neural network layers.** One layer transforms the input with
$W_1\mathbf{x}$, the next one transforms the result with $W_2$. Without a
non-linear operation (an activation function) in between, two layers
would equal a single layer:

$$
W_2(W_1\mathbf{x}) = (W_2 W_1)\mathbf{x}
$$

Stack a hundred layers and, as long as they stay linear, they are only as
powerful as one matrix. That is exactly why neural networks put curved
functions such as ReLU between the layers.

**Image processing.** Rotating, enlarging or mirroring a photo means
multiplying every pixel's coordinates by a matrix. Data augmentation
(training a model on rotated and mirrored copies of the same photo) is
done with these transformations.

**Computational cost.** In an $(m \times n)(n \times p)$ product each
entry takes $n$ multiplications, $m \cdot n \cdot p$ in total. For two
$1000 \times 1000$ matrices that is a billion multiplications. Graphics
cards (GPUs) are used in deep learning because they are designed to do
huge numbers of independent multiply–adds at the same time.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$AB = BA$</p>
      <p>$(AB)^\mathsf{T} = A^\mathsf{T} B^\mathsf{T}$</p>
      <p>$A^2$ = squaring the entries</p>
      <p>Multiplying $AB$ entry by entry</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>Usually $AB \ne BA$</p>
      <p>$(AB)^\mathsf{T} = B^\mathsf{T} A^\mathsf{T}$</p>
      <p>$A^2 = AA$, row times column</p>
      <p>$c_{ij}$ = row $i$ · column $j$</p>
    </div>
  </div>
  <figcaption>Matrix multiplication looks like multiplying numbers, but the order and the entry rule are different.</figcaption>
</figure>

- **Starting to multiply without checking sizes.** First check that the
  inner numbers match, then write down the size of the result (the outer
  numbers).
- **Multiplying entry by entry.** The product of $\begin{bmatrix} 1 & 2
  \\ 3 & 4 \end{bmatrix}$ and $\begin{bmatrix} 5 & 6 \\ 7 & 8
  \end{bmatrix}$ is not $\begin{bmatrix} 5 & 12 \\ 21 & 32
  \end{bmatrix}$. Entry-by-entry multiplication has a name of its own (the
  Hadamard product, $\odot$), but it is not matrix multiplication.
- **Reading the order of transformations backwards.** In $AB\mathbf{x}$,
  $B$ is applied first.
- **Forgetting the order in the transpose.** $(AB)^\mathsf{T} =
  B^\mathsf{T} A^\mathsf{T}$.

## Summary

- Size: $(m \times n)(n \times p) = m \times p$; the inner numbers must match.
- Entry: $c_{ij}$ = row $i$ of $A$ · column $j$ of $B$.
- Column view: column $j$ of $AB$ is $A\mathbf{b}_j$.
- Usually $AB \ne BA$; associativity and distributivity hold; $AI = IA = A$.
- $(AB)^\mathsf{T} = B^\mathsf{T} A^\mathsf{T}$; $A^2 = AA$.
- A $2 \times 2$ matrix is a transformation: its columns are where $\mathbf{e}_1$ and $\mathbf{e}_2$ go.
- Scaling, rotation ($R_\theta$), reflection, shear, projection.
- $A(B\mathbf{x}) = (AB)\mathbf{x}$: transformations in a row = product, read right to left.
- ML: $XW$ covers every example and model; linear layers collapse into one matrix.
