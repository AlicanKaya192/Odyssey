# Matrices

Suppose you have information about three houses: each one's floor area,
number of rooms and age. In the previous chapters we described each
house with a vector. Write the three vectors one under the other and a
**table** appears:

| | Area | Rooms | Age |
|---|---|---|---|
| House 1 | 120 | 3 | 10 |
| House 2 | 80 | 2 | 25 |
| House 3 | 150 | 4 | 5 |

The body of this table, made of numbers, is a **matrix**. In machine
learning data is nearly always laid out like this: every row is an
example (a house, a customer, a photo) and every column a feature. The
weights a neural network learns are matrices, and so are the pixels of
a photo.

In this chapter we will see what a matrix is, how to read one, the
special matrices, adding matrices and multiplying them by a scalar, the
**transpose**, and how a matrix is multiplied by a vector. Multiplying
two matrices together, and how matrices rotate and stretch the plane,
come in the next chapter.

Prerequisites: the Vectors and Dot Product chapters.

## Definition and notation

A **matrix** is a rectangular table of numbers arranged in rows and
columns. It is named with a capital letter and written inside square
brackets:

$$
A = \begin{bmatrix} 5 & 2 & 0 & 1 \\ 3 & 7 & 4 & 6 \\ 1 & 8 & 9 & 2 \end{bmatrix}
$$

### Size: rows first, then columns

$A$ has 3 rows and 4 columns; its size is written **$3 \times 4$**
("three by four"). The order is always the same: **rows first, then
columns**. A $4 \times 3$ matrix is a different shape: 4 rows, 3
columns.

The set of real matrices of size $m \times n$ is written
$\mathbb{R}^{m \times n}$; $A \in \mathbb{R}^{3 \times 4}$.

### Entry: $a_{ij}$

Each number in a matrix is called an **entry** (or element). The entry
where row $i$ meets column $j$ is written with a small letter and two
subscripts: $a_{ij}$. Same order again: **row number first, then column
number**.

<figure class="fig">
<svg viewBox="0 0 400 224" width="400"><rect class="box" x="110" y="44" width="38" height="38"/><text class="ink" x="129.0" y="68.0" font-size="15" text-anchor="middle">5</text><rect class="box" x="148" y="44" width="38" height="38"/><text class="ink" x="167.0" y="68.0" font-size="15" text-anchor="middle">2</text><rect class="box" x="186" y="44" width="38" height="38"/><text class="ink" x="205.0" y="68.0" font-size="15" text-anchor="middle">0</text><rect class="box" x="224" y="44" width="38" height="38"/><text class="ink" x="243.0" y="68.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="110" y="82" width="38" height="38"/><text class="ink" x="129.0" y="106.0" font-size="15" text-anchor="middle">3</text><rect class="box" x="148" y="82" width="38" height="38"/><text class="ink" x="167.0" y="106.0" font-size="15" text-anchor="middle">7</text><rect class="box" x="186" y="82" width="38" height="38"/><text class="ink" x="205.0" y="106.0" font-size="15" text-anchor="middle">4</text><rect class="box" x="224" y="82" width="38" height="38"/><text class="ink" x="243.0" y="106.0" font-size="15" text-anchor="middle">6</text><rect class="box" x="110" y="120" width="38" height="38"/><text class="ink" x="129.0" y="144.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="148" y="120" width="38" height="38"/><text class="ink" x="167.0" y="144.0" font-size="15" text-anchor="middle">8</text><rect class="box" x="186" y="120" width="38" height="38"/><text class="ink" x="205.0" y="144.0" font-size="15" text-anchor="middle">9</text><rect class="box" x="224" y="120" width="38" height="38"/><text class="ink" x="243.0" y="144.0" font-size="15" text-anchor="middle">2</text><rect class="curve" x="107" y="79" width="158" height="44" rx="4"/><rect class="curve2" x="183" y="41" width="44" height="120" rx="4"/><text class="ink" x="98" y="106.0" font-size="13" text-anchor="end">row 2</text><text class="ink" x="205.0" y="30" font-size="13" text-anchor="middle">column 3</text><text class="ink" x="205.0" y="184" font-size="14" text-anchor="middle">a₂₃ = 4</text><text class="dim" x="186" y="210" font-size="12" text-anchor="middle">3 rows × 4 columns</text></svg>
  <figcaption>The purple frame is row 2, the orange frame column 3. The entry where they meet is $a_{23} = 4$.</figcaption>
</figure>

In the same matrix $a_{11} = 5$ (top-left corner), $a_{14} = 1$ (end of
the first row), $a_{32} = 8$. $a_{23}$ and $a_{32}$ are different
entries: one is "row 2, column 3", the other "row 3, column 2".

A general $m \times n$ matrix:

$$
A = \begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}
$$

It is also written briefly as $A = [a_{ij}]$.

**Writing it on one line.** Where formulas cannot be typeset (plain
text, code, this chapter's quiz questions) a matrix is written row by
row, with the rows separated by **semicolons**: `[1 2; 3 4]` is the
$2 \times 2$ matrix whose row 1 is $(1, 2)$ and row 2 is $(3, 4)$.
`[1; 2]` is a column with two rows, `[1 2]` a single-row row vector.

### Rows and columns are vectors

Every row of a matrix is a vector, and so is every column. In the house
table, row 1 is $(120, 3, 10)$, the feature vector of house 1; column 1
is $(120, 80, 150)$, the areas of all the houses. A matrix can be seen as
**row vectors stacked on top of each other** or as **column vectors
placed side by side**. Both views are right, and by the end of this
chapter we will need both.

**A vector is a matrix too:** a vector with $n$ components is written as
an $n \times 1$ **column vector**. A $1 \times n$ matrix with a single
row is called a **row vector**.

$$
\mathbf{x} = \begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix} \;(3 \times 1)
\qquad
\begin{bmatrix} 1 & 2 & 3 \end{bmatrix} \;(1 \times 3)
$$

In linear algebra "vector" means a **column vector** unless stated
otherwise.

## Special matrices

Some matrices appear so often that they have their own names.

| Name | Definition | Example |
|---|---|---|
| Square matrix | Number of rows = number of columns ($n \times n$) | $\begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$ |
| Zero matrix $O$ | Every entry is $0$ | $\begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}$ |
| Diagonal matrix | Square; every entry off the diagonal is $0$ | $\begin{bmatrix} 3 & 0 \\ 0 & -1 \end{bmatrix}$ |
| Identity matrix $I$ | Diagonal; the diagonal is all $1$ | $\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$ |
| Upper triangular | Square; below the diagonal is $0$ | $\begin{bmatrix} 2 & 5 \\ 0 & 7 \end{bmatrix}$ |
| Lower triangular | Square; above the diagonal is $0$ | $\begin{bmatrix} 2 & 0 \\ 5 & 7 \end{bmatrix}$ |
| Symmetric | Square; $a_{ij} = a_{ji}$ | $\begin{bmatrix} 2 & 7 \\ 7 & 5 \end{bmatrix}$ |

The **diagonal** (the main diagonal) means the entries running from top
left to bottom right: $a_{11}, a_{22}, a_{33}, \dots$ It only makes sense
for square matrices.

The **identity matrix** $I$ is the matrix counterpart of the number $1$:
multiplying a vector by it leaves the vector unchanged (we will see this
at the end of the chapter). When the size needs saying, write $I_3$:

$$
I_3 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

A **symmetric** matrix is the same as its mirror image across the
diagonal. Distance tables are symmetric: the distance from Istanbul to
Ankara equals the distance from Ankara to Istanbul. The **covariance
matrix** we will meet in the statistics chapters is always symmetric
too.

## Equality

Two matrices are equal **if and only if** they have the same size and
all their corresponding entries are equal.

$$
\begin{bmatrix} x & 3 \\ 1 & y \end{bmatrix} = \begin{bmatrix} 5 & 3 \\ 1 & -2 \end{bmatrix}
\;\Rightarrow\; x = 5,\; y = -2
$$

$\begin{bmatrix} 1 & 2 \end{bmatrix}$ and $\begin{bmatrix} 1 \\ 2 \end{bmatrix}$
contain the same numbers but are **not** equal: one is $1 \times 2$,
the other $2 \times 1$.

## Addition and subtraction

Two matrices of the same size are added **entry by entry**: the numbers
in matching positions are added and written in the same position:

$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
\qquad
B = \begin{bmatrix} 5 & 0 \\ 1 & 2 \end{bmatrix}
$$

$$
A + B = \begin{bmatrix} 1 + 5 & 2 + 0 \\ 3 + 1 & 4 + 2 \end{bmatrix} = \begin{bmatrix} 6 & 2 \\ 4 & 6 \end{bmatrix}
$$

Subtraction is the same: $A - B = \begin{bmatrix} -4 & 2 \\ 2 & 2 \end{bmatrix}$.

This is exactly vector addition; the matrix simply behaves like a vector
with more components. Two matrices of different sizes **cannot** be
added (not even $2 \times 3$ and $3 \times 2$): some entries would have
no partner.

The rules for numbers hold:

| Rule | Written as |
|---|---|
| Commutativity | $A + B = B + A$ |
| Associativity | $(A + B) + C = A + (B + C)$ |
| Zero matrix | $A + O = A$ |
| Negative | $A + (-A) = O$ |

**Meaning:** add the sales tables of two months (row = shop, column =
product) and you get the two-month total sales table. Averaging two
photos is also adding entry by entry and dividing by two.

## Multiplying by a scalar

Multiplying a matrix by a number means multiplying every entry by that
number:

$$
3A = 3 \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} = \begin{bmatrix} 3 & 6 \\ 9 & 12 \end{bmatrix}
$$

Again the same as for vectors. Multiplying every entry of a price table
by $1.2$ raises every price by 20%. The rules:

| Rule | Written as |
|---|---|
| Distributivity | $c(A + B) = cA + cB$ |
| Distributivity | $(c + d)A = cA + dA$ |
| Associativity | $c(dA) = (cd)A$ |

Addition and scaling together build **linear combinations**: $2A - B$,
$\tfrac{1}{2}(A + B)$ and so on.

## The transpose

The **transpose** of a matrix is the matrix whose rows are the original
columns and whose columns are the original rows. It is written
$A^\mathsf{T}$ ("A transpose").

<figure class="fig">
<svg viewBox="0 0 400 173" width="400"><rect class="box" x="30" y="62" width="38" height="38"/><text class="ink" x="49.0" y="86.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="68" y="62" width="38" height="38"/><text class="ink" x="87.0" y="86.0" font-size="15" text-anchor="middle">2</text><rect class="box" x="106" y="62" width="38" height="38"/><text class="ink" x="125.0" y="86.0" font-size="15" text-anchor="middle">3</text><rect class="box" x="30" y="100" width="38" height="38"/><text class="ink" x="49.0" y="124.0" font-size="15" text-anchor="middle">4</text><rect class="box" x="68" y="100" width="38" height="38"/><text class="ink" x="87.0" y="124.0" font-size="15" text-anchor="middle">5</text><rect class="box" x="106" y="100" width="38" height="38"/><text class="ink" x="125.0" y="124.0" font-size="15" text-anchor="middle">6</text><rect class="box" x="290" y="43" width="38" height="38"/><text class="ink" x="309.0" y="67.0" font-size="15" text-anchor="middle">1</text><rect class="box" x="328" y="43" width="38" height="38"/><text class="ink" x="347.0" y="67.0" font-size="15" text-anchor="middle">4</text><rect class="box" x="290" y="81" width="38" height="38"/><text class="ink" x="309.0" y="105.0" font-size="15" text-anchor="middle">2</text><rect class="box" x="328" y="81" width="38" height="38"/><text class="ink" x="347.0" y="105.0" font-size="15" text-anchor="middle">5</text><rect class="box" x="290" y="119" width="38" height="38"/><text class="ink" x="309.0" y="143.0" font-size="15" text-anchor="middle">3</text><rect class="box" x="328" y="119" width="38" height="38"/><text class="ink" x="347.0" y="143.0" font-size="15" text-anchor="middle">6</text><rect class="curve" x="27" y="59" width="120" height="39" rx="4"/><rect class="curve2" x="27" y="102" width="120" height="39" rx="4"/><rect class="curve" x="287" y="40" width="39" height="120" rx="4"/><rect class="curve2" x="330" y="40" width="39" height="120" rx="4"/><text class="ink" x="87.0" y="46" font-size="13" text-anchor="middle">A  (2 × 3)</text><text class="ink" x="328" y="27" font-size="13" text-anchor="middle">Aᵀ  (3 × 2)</text><line class="curve3" x1="166" y1="100" x2="259" y2="100"/><polygon class="dim" points="268,100 257,95 257,105"/></svg>
  <figcaption>Row 1 of $A$ (purple) becomes column 1 of $A^\mathsf{T}$, and row 2 (orange) becomes column 2. The transpose of a $2 \times 3$ matrix is $3 \times 2$.</figcaption>
</figure>

$$
A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
\qquad
A^\mathsf{T} = \begin{bmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{bmatrix}
$$

In terms of entries: the entry in row $i$, column $j$ of the transpose is
the entry in row $j$, column $i$ of the original.

$$
(A^\mathsf{T})_{ij} = a_{ji}
$$

The transpose of an $m \times n$ matrix is $n \times m$. For a square
matrix, transposing **mirrors the matrix across its diagonal**: the
diagonal stays put and the other entries swap with their partners on the
opposite side.

### Rules of the transpose

| Rule | Written as |
|---|---|
| Transposing twice | $(A^\mathsf{T})^\mathsf{T} = A$ |
| Sum | $(A + B)^\mathsf{T} = A^\mathsf{T} + B^\mathsf{T}$ |
| Scalar | $(cA)^\mathsf{T} = c\,A^\mathsf{T}$ |
| Symmetric | $A$ symmetric $\iff A^\mathsf{T} = A$ |

**The transpose of a column vector is a row vector:**

$$
\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix}^\mathsf{T} = \begin{bmatrix} 1 & 2 & 3 \end{bmatrix}
$$

Books write $\mathbf{x}^\mathsf{T}$ instead of writing a row vector out
separately. That is also why the dot product of two column vectors often
appears as $\mathbf{a}^\mathsf{T} \mathbf{b}$: a row vector times a
column vector, and the result is a single number.

## Multiplying a matrix by a vector

There are two ways to look at multiplying a matrix by a vector. Both
give the same result but they tell you different things.

### The size rule

An $m \times n$ matrix can only be multiplied by a vector with **$n$
components**, and the result is a vector with **$m$ components**:

$$
\underbrace{A}_{m \times n}\;\underbrace{\mathbf{x}}_{n \times 1} = \underbrace{\mathbf{y}}_{m \times 1}
$$

The matrix's **number of columns** must equal the vector's **number of
components**. The length of the result is the matrix's **number of
rows**.

### The row view: a dot product with each row

Component $i$ of the result is the dot product of row $i$ of $A$ with
$\mathbf{x}$:

$$
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
\begin{bmatrix} 1 \\ 0 \\ -1 \end{bmatrix}
= \begin{bmatrix} 1 \cdot 1 + 2 \cdot 0 + 3 \cdot (-1) \\ 4 \cdot 1 + 5 \cdot 0 + 6 \cdot (-1) \end{bmatrix}
= \begin{bmatrix} -2 \\ -2 \end{bmatrix}
$$

A $2 \times 3$ matrix, a vector with 3 components, a result with 2
components. The dot product from the previous chapter is repeated here
once for each row.

### The column view: a linear combination of the columns

The same product is the sum of the **columns** of $A$ weighted by the
components of $\mathbf{x}$:

$$
A\mathbf{x} = x_1\,\mathbf{a}_1 + x_2\,\mathbf{a}_2 + \cdots + x_n\,\mathbf{a}_n
$$

Here $\mathbf{a}_j$ is column $j$ of $A$. An example:

$$
\begin{bmatrix} 2 & -1 \\ 1 & 1 \end{bmatrix}
\begin{bmatrix} 1 \\ 2 \end{bmatrix}
= 1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} + 2 \begin{bmatrix} -1 \\ 1 \end{bmatrix}
= \begin{bmatrix} 0 \\ 3 \end{bmatrix}
$$

<figure class="fig">
<svg viewBox="0 0 252 252" width="252"><line class="grid" x1="26" y1="226" x2="26" y2="26"/><line class="grid" x1="66" y1="226" x2="66" y2="26"/><line class="line" x1="106" y1="226" x2="106" y2="26"/><line class="grid" x1="146" y1="226" x2="146" y2="26"/><line class="grid" x1="186" y1="226" x2="186" y2="26"/><line class="grid" x1="226" y1="226" x2="226" y2="26"/><line class="grid" x1="26" y1="226" x2="226" y2="226"/><line class="line" x1="26" y1="186" x2="226" y2="186"/><line class="grid" x1="26" y1="146" x2="226" y2="146"/><line class="grid" x1="26" y1="106" x2="226" y2="106"/><line class="grid" x1="26" y1="66" x2="226" y2="66"/><line class="grid" x1="26" y1="26" x2="226" y2="26"/><text class="dim" x="26" y="200" font-size="10" text-anchor="middle">-2</text><text class="dim" x="66" y="200" font-size="10" text-anchor="middle">-1</text><text class="dim" x="146" y="200" font-size="10" text-anchor="middle">1</text><text class="dim" x="186" y="200" font-size="10" text-anchor="middle">2</text><text class="dim" x="226" y="200" font-size="10" text-anchor="middle">3</text><text class="dim" x="100" y="230" font-size="10" text-anchor="end">-1</text><text class="dim" x="100" y="150" font-size="10" text-anchor="end">1</text><text class="dim" x="100" y="110" font-size="10" text-anchor="end">2</text><text class="dim" x="100" y="70" font-size="10" text-anchor="end">3</text><text class="dim" x="100" y="30" font-size="10" text-anchor="end">4</text><line class="curve4" x1="106" y1="186" x2="106.0" y2="74.8"/><polygon class="dot3" points="106,66 110.5,76.0 101.5,76.0"/><line class="curve" x1="106" y1="186" x2="178.1" y2="149.9"/><polygon class="dot" points="186,146 179.0,154.5 175.0,146.5"/><line class="curve2" x1="186" y1="146" x2="112.2" y2="72.2"/><polygon class="dot2" points="106,66 116.3,69.9 109.9,76.3"/><text class="ink" x="194" y="152" font-size="13" text-anchor="start">1 · a₁</text><text class="ink" x="154" y="102" font-size="13" text-anchor="start">2 · a₂</text><text class="ink" x="116" y="58" font-size="14" text-anchor="start">Ax</text></svg>
  <figcaption>First walk the 1st column $(2, 1)$ (purple), then twice the 2nd column, $(-2, 2)$ (orange). Where you arrive is $A\mathbf{x} = (0, 3)$ (green).</figcaption>
</figure>

Checking with the row view: $2 \cdot 1 + (-1) \cdot 2 = 0$ and
$1 \cdot 1 + 1 \cdot 2 = 3$. ✓

The column view says something very important: **$A\mathbf{x}$ is always
a vector that can be built from the columns of $A$.** The question "for
which $\mathbf{x}$ is $A\mathbf{x} = \mathbf{b}$?" is the same as "with
which coefficients do I build $\mathbf{b}$ from the columns?". The "find
the coefficients" problem in the Vectors chapter was exactly this; in
the Gaussian elimination chapter we will solve this question
systematically.

### Multiplying by the identity matrix

$$
I\mathbf{x} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} 7 \\ -3 \end{bmatrix}
= 7 \begin{bmatrix} 1 \\ 0 \end{bmatrix} - 3 \begin{bmatrix} 0 \\ 1 \end{bmatrix}
= \begin{bmatrix} 7 \\ -3 \end{bmatrix}
$$

The columns of the identity matrix are the basic unit vectors; the
coefficients that build $\mathbf{x}$ from them are $\mathbf{x}$'s own
components. That is why $I\mathbf{x} = \mathbf{x}$.

### Rules

| Rule | Written as |
|---|---|
| Distributes over vectors | $A(\mathbf{x} + \mathbf{y}) = A\mathbf{x} + A\mathbf{y}$ |
| Scalar comes out | $A(c\,\mathbf{x}) = c\,(A\mathbf{x})$ |
| Distributes over matrices | $(A + B)\mathbf{x} = A\mathbf{x} + B\mathbf{x}$ |

The first two rules say that multiplying by a matrix is a **linear**
operation. That is where the name "linear algebra" comes from.

## Matrices in machine learning

**The data matrix.** With $n$ examples and $d$ features, the data is an
$n \times d$ matrix: $X \in \mathbb{R}^{n \times d}$. Row $i$ is the
feature vector of example $i$; column $j$ holds the values of feature $j$
across all examples.

**All predictions in one product.** If a linear model's weight vector is
$\mathbf{w}$, the prediction for one example is the dot product of that
example's row with $\mathbf{w}$. By the row view, that is exactly what
$X\mathbf{w}$ does:

$$
X = \begin{bmatrix} 1.2 & 3 \\ 0.8 & 2 \\ 1.5 & 4 \end{bmatrix}
\qquad
\mathbf{w} = \begin{bmatrix} 100 \\ 20 \end{bmatrix}
\qquad
X\mathbf{w} = \begin{bmatrix} 180 \\ 120 \\ 230 \end{bmatrix}
$$

The first column is the area in hundreds of square metres, the second
the number of rooms; the predictions are prices in thousands. The
prediction for the first house is $1.2 \cdot 100 + 3 \cdot 20 = 180$.
The prices of all three houses came from a single matrix–vector product.
With a million houses the notation is the same: $\hat{\mathbf{y}} = X\mathbf{w}$.

**Images.** A greyscale photo is a matrix holding the brightness of each
pixel. A $28 \times 28$ pixel handwritten digit is a matrix of 784
numbers; a colour photo is three matrices, one for each colour channel
(red, green, blue).

<figure class="fig">
<svg viewBox="0 0 400 190" width="400"><rect class="box" x="20" y="20" width="30" height="30"/><rect class="ink" x="20" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="50" y="20" width="30" height="30"/><rect class="ink" x="50" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="80" y="20" width="30" height="30"/><rect class="ink" x="80" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="110" y="20" width="30" height="30"/><rect class="ink" x="110" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="140" y="20" width="30" height="30"/><rect class="ink" x="140" y="20" width="30" height="30" opacity="1.0"/><rect class="box" x="20" y="50" width="30" height="30"/><rect class="box" x="50" y="50" width="30" height="30"/><rect class="box" x="80" y="50" width="30" height="30"/><rect class="box" x="110" y="50" width="30" height="30"/><rect class="ink" x="110" y="50" width="30" height="30" opacity="0.78"/><rect class="box" x="140" y="50" width="30" height="30"/><rect class="ink" x="140" y="50" width="30" height="30" opacity="0.22"/><rect class="box" x="20" y="80" width="30" height="30"/><rect class="box" x="50" y="80" width="30" height="30"/><rect class="box" x="80" y="80" width="30" height="30"/><rect class="ink" x="80" y="80" width="30" height="30" opacity="0.67"/><rect class="box" x="110" y="80" width="30" height="30"/><rect class="ink" x="110" y="80" width="30" height="30" opacity="0.33"/><rect class="box" x="140" y="80" width="30" height="30"/><rect class="box" x="20" y="110" width="30" height="30"/><rect class="box" x="50" y="110" width="30" height="30"/><rect class="ink" x="50" y="110" width="30" height="30" opacity="0.56"/><rect class="box" x="80" y="110" width="30" height="30"/><rect class="ink" x="80" y="110" width="30" height="30" opacity="0.44"/><rect class="box" x="110" y="110" width="30" height="30"/><rect class="box" x="140" y="110" width="30" height="30"/><rect class="box" x="20" y="140" width="30" height="30"/><rect class="box" x="50" y="140" width="30" height="30"/><rect class="ink" x="50" y="140" width="30" height="30" opacity="1.0"/><rect class="box" x="80" y="140" width="30" height="30"/><rect class="box" x="110" y="140" width="30" height="30"/><rect class="box" x="140" y="140" width="30" height="30"/><rect class="box" x="230" y="20" width="30" height="30"/><text class="ink" x="245.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="260" y="20" width="30" height="30"/><text class="ink" x="275.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="290" y="20" width="30" height="30"/><text class="ink" x="305.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="320" y="20" width="30" height="30"/><text class="ink" x="335.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="350" y="20" width="30" height="30"/><text class="ink" x="365.0" y="40.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="230" y="50" width="30" height="30"/><text class="dim" x="245.0" y="70.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="260" y="50" width="30" height="30"/><text class="dim" x="275.0" y="70.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="290" y="50" width="30" height="30"/><text class="dim" x="305.0" y="70.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="320" y="50" width="30" height="30"/><text class="ink" x="335.0" y="70.0" font-size="14" text-anchor="middle">7</text><rect class="box" x="350" y="50" width="30" height="30"/><text class="ink" x="365.0" y="70.0" font-size="14" text-anchor="middle">2</text><rect class="box" x="230" y="80" width="30" height="30"/><text class="dim" x="245.0" y="100.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="260" y="80" width="30" height="30"/><text class="dim" x="275.0" y="100.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="290" y="80" width="30" height="30"/><text class="ink" x="305.0" y="100.0" font-size="14" text-anchor="middle">6</text><rect class="box" x="320" y="80" width="30" height="30"/><text class="ink" x="335.0" y="100.0" font-size="14" text-anchor="middle">3</text><rect class="box" x="350" y="80" width="30" height="30"/><text class="dim" x="365.0" y="100.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="230" y="110" width="30" height="30"/><text class="dim" x="245.0" y="130.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="260" y="110" width="30" height="30"/><text class="ink" x="275.0" y="130.0" font-size="14" text-anchor="middle">5</text><rect class="box" x="290" y="110" width="30" height="30"/><text class="ink" x="305.0" y="130.0" font-size="14" text-anchor="middle">4</text><rect class="box" x="320" y="110" width="30" height="30"/><text class="dim" x="335.0" y="130.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="350" y="110" width="30" height="30"/><text class="dim" x="365.0" y="130.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="230" y="140" width="30" height="30"/><text class="dim" x="245.0" y="160.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="260" y="140" width="30" height="30"/><text class="ink" x="275.0" y="160.0" font-size="14" text-anchor="middle">9</text><rect class="box" x="290" y="140" width="30" height="30"/><text class="dim" x="305.0" y="160.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="320" y="140" width="30" height="30"/><text class="dim" x="335.0" y="160.0" font-size="14" text-anchor="middle">0</text><rect class="box" x="350" y="140" width="30" height="30"/><text class="dim" x="365.0" y="160.0" font-size="14" text-anchor="middle">0</text><line class="curve3" x1="182" y1="95.0" x2="209" y2="95.0"/><polygon class="dim" points="218,95.0 207,90.0 207,100.0"/></svg>
  <figcaption>On the left a "7" of $5 \times 5$ pixels, on the right the numbers of the same image (0 empty, 9 darkest). A computer sees the image as it appears on the right.</figcaption>
</figure>

Making a photo brighter is scaling, averaging two photos is addition and
scaling, and flipping a photo across its diagonal is the transpose.

**A neural network layer.** Every neuron in a layer computes the dot
product of the inputs with its own weights. Stack the weights of all the
neurons as the rows of a matrix and the whole layer becomes a single
product $W\mathbf{x}$.

## The trace

The **trace** of a square matrix is the sum of its diagonal entries:

$$
\operatorname{tr}\begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix} = 4 + 3 = 7
$$

For now it is just a definition; in the eigenvalues chapter we will see
that the trace equals the sum of the eigenvalues.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$3 \times 4$: 3 columns, 4 rows</p>
      <p>$a_{23}$: column 2, row 3</p>
      <p>A $2 \times 3$ and a $3 \times 2$ matrix can be added</p>
      <p>A $2 \times 3$ matrix times a vector with 2 components</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>$3 \times 4$: 3 rows, 4 columns</p>
      <p>$a_{23}$: row 2, column 3</p>
      <p>For addition the sizes must be exactly the same</p>
      <p>A $2 \times 3$ matrix is multiplied by a vector with 3 components</p>
    </div>
  </div>
  <figcaption>In sizes and subscripts the order is always the same: rows first, then columns.</figcaption>
</figure>

- **Mixing up rows and columns.** Both the size and the entry name the
  row first.
- **Thinking the transpose just swaps things around.** The transpose of a
  $2 \times 3$ matrix is not $2 \times 3$ again but $3 \times 2$.
- **Not checking sizes in a matrix–vector product.** If the matrix's
  number of columns differs from the vector's number of components, the
  product is undefined.
- **Getting the length of the result wrong.** The result has as many
  components as the matrix has rows.

## Summary

- Matrix: numbers arranged in rows and columns. Size $m \times n$, rows first.
- $a_{ij}$: row $i$, column $j$.
- Special matrices: square, zero, diagonal, identity $I$, triangular, symmetric.
- Addition and scaling work entry by entry; addition needs equal sizes.
- Transpose: rows become columns, $(A^\mathsf{T})_{ij} = a_{ji}$, size $n \times m$.
- $A\mathbf{x}$: in the row view a dot product with each row; in the column view a linear combination of the columns.
- Size rule: $(m \times n)$ times $n$ components $=$ $m$ components.
- ML: data matrix $X$, all predictions $X\mathbf{w}$, images, a neural network layer $W\mathbf{x}$.
