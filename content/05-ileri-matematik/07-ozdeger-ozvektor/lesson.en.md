# Eigenvalues and Eigenvectors

When multiplied by a matrix, most vectors both grow or shrink and **change
direction**. But most matrices have a few special vectors whose direction
they never change: the matrix only stretches, shrinks or flips them. These
vectors are called **eigenvectors**, and the amount of stretching is the
**eigenvalue**.

Why do they matter so much? Because they show a matrix's "skeleton". A
complicated-looking transformation, seen in the basis of its
eigenvectors, is nothing more than multiplying each direction by its own
number. This idea is everywhere in machine learning: PCA finds the
directions in which data spreads most with the eigenvectors of a matrix,
Google's PageRank ranks the most important pages of the web with an
eigenvector, and eigenvalues tell you whether training a model will be
stable.

Prerequisites: the Determinants and Inverse Matrices, and Linear
Independence and Rank sections.

## Definition

For a square matrix $A$, if a non-zero vector $\mathbf{v}$ and a number
$\lambda$ satisfy

$$
A\mathbf{v} = \lambda\mathbf{v}
$$

then $\mathbf{v}$ is called an **eigenvector** of $A$ and $\lambda$
(lambda) the corresponding **eigenvalue**.

In words: applying $A$ to $\mathbf{v}$ is the same as multiplying
$\mathbf{v}$ by a number. The result stays **on the same line** as
$\mathbf{v}$.

- $\lambda > 1$: the vector grows.
- $0 < \lambda < 1$: it shrinks.
- $\lambda < 0$: it flips to the opposite direction (still on the same line).
- $\lambda = 0$: it goes to zero; $\mathbf{v}$ is in the null space.

$\mathbf{v} = \mathbf{0}$ is excluded: $A\mathbf{0} = \lambda\mathbf{0}$
holds for every $\lambda$ and says nothing.

### An example

$$
A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}
$$

Try three vectors:

$$
\begin{aligned}
A \begin{bmatrix} 1 \\ 1 \end{bmatrix} &= \begin{bmatrix} 3 \\ 3 \end{bmatrix} = 3 \begin{bmatrix} 1 \\ 1 \end{bmatrix} \\
A \begin{bmatrix} 1 \\ -1 \end{bmatrix} &= \begin{bmatrix} 1 \\ -1 \end{bmatrix} = 1 \begin{bmatrix} 1 \\ -1 \end{bmatrix} \\
A \begin{bmatrix} 1 \\ 0 \end{bmatrix} &= \begin{bmatrix} 2 \\ 1 \end{bmatrix}
\end{aligned}
$$

$(1, 1)$ is an eigenvector with eigenvalue $3$: it grows three times.
$(1, -1)$ is an eigenvector with eigenvalue $1$: it does not change at
all. $(1, 0)$ is **not** an eigenvector: $(2, 1)$ is not a multiple of it,
its direction changed.

<figure class="fig">
<svg viewBox="0 0 420 222" width="420"><line class="grid" x1="16" y1="194" x2="16" y2="14"/><line class="grid" x1="46" y1="194" x2="46" y2="14"/><line class="line" x1="76" y1="194" x2="76" y2="14"/><line class="grid" x1="106" y1="194" x2="106" y2="14"/><line class="grid" x1="136" y1="194" x2="136" y2="14"/><line class="grid" x1="166" y1="194" x2="166" y2="14"/><line class="grid" x1="196" y1="194" x2="196" y2="14"/><line class="grid" x1="16" y1="194" x2="196" y2="194"/><line class="grid" x1="16" y1="164" x2="196" y2="164"/><line class="line" x1="16" y1="134" x2="196" y2="134"/><line class="grid" x1="16" y1="104" x2="196" y2="104"/><line class="grid" x1="16" y1="74" x2="196" y2="74"/><line class="grid" x1="16" y1="44" x2="196" y2="44"/><line class="grid" x1="16" y1="14" x2="196" y2="14"/><line class="curve3" stroke-dasharray="4 3" x1="16.0" y1="194.0" x2="196.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" x1="16.0" y1="74.0" x2="136.0" y2="194.0"/><line class="curve" x1="76" y1="134" x2="100.9" y2="109.1"/><polygon class="dot" points="106,104 102.8,112.4 97.6,107.2"/><line class="curve2" x1="76" y1="134" x2="100.9" y2="158.9"/><polygon class="dot2" points="106,164 97.6,160.8 102.8,155.6"/><line class="curve4" x1="76" y1="134" x2="98.8" y2="134.0"/><polygon class="dot3" points="106,134 97.8,137.7 97.8,130.3"/><text class="ink" x="111" y="104" font-size="12" text-anchor="start">v₁</text><text class="ink" x="111" y="172" font-size="12" text-anchor="start">v₂</text><text class="ink" x="111" y="138" font-size="12" text-anchor="start">u</text><text class="ink" x="106.0" y="212" font-size="12" text-anchor="middle">Before</text><line class="grid" x1="222" y1="194" x2="222" y2="14"/><line class="grid" x1="252" y1="194" x2="252" y2="14"/><line class="line" x1="282" y1="194" x2="282" y2="14"/><line class="grid" x1="312" y1="194" x2="312" y2="14"/><line class="grid" x1="342" y1="194" x2="342" y2="14"/><line class="grid" x1="372" y1="194" x2="372" y2="14"/><line class="grid" x1="402" y1="194" x2="402" y2="14"/><line class="grid" x1="222" y1="194" x2="402" y2="194"/><line class="grid" x1="222" y1="164" x2="402" y2="164"/><line class="line" x1="222" y1="134" x2="402" y2="134"/><line class="grid" x1="222" y1="104" x2="402" y2="104"/><line class="grid" x1="222" y1="74" x2="402" y2="74"/><line class="grid" x1="222" y1="44" x2="402" y2="44"/><line class="grid" x1="222" y1="14" x2="402" y2="14"/><line class="curve3" stroke-dasharray="4 3" x1="222.0" y1="194.0" x2="402.0" y2="14.0"/><line class="curve3" stroke-dasharray="4 3" x1="222.0" y1="74.0" x2="342.0" y2="194.0"/><line class="curve" x1="282" y1="134" x2="366.9" y2="49.1"/><polygon class="dot" points="372,44 368.8,52.4 363.6,47.2"/><line class="curve2" x1="282" y1="134" x2="306.9" y2="158.9"/><polygon class="dot2" points="312,164 303.6,160.8 308.8,155.6"/><line class="curve4" x1="282" y1="134" x2="335.6" y2="107.2"/><polygon class="dot3" points="342,104 336.3,111.0 333.0,104.4"/><line class="curve3" stroke-dasharray="4 3" x1="282" y1="134" x2="304.8" y2="134.0"/><polygon class="dim" points="312,134 303.8,137.7 303.8,130.3"/><text class="ink" x="366" y="44" font-size="11" text-anchor="end">Av₁ = 3v₁</text><text class="ink" x="317" y="174" font-size="11" text-anchor="start">Av₂ = v₂</text><text class="ink" x="347" y="108" font-size="11" text-anchor="start">Au</text><text class="ink" x="312.0" y="212" font-size="12" text-anchor="middle">After applying A = [2 1; 1 2]</text></svg>
  <figcaption>The dashed lines are the lines of the two eigenvectors. Under $A$, $\mathbf{v}_1 = (1, 1)$ (purple) stretches three times along its own line, and $\mathbf{v}_2 = (1, -1)$ (orange) stays where it is. The ordinary vector $\mathbf{u} = (1, 0)$ (green) changes direction and goes to $(2, 1)$.</figcaption>
</figure>

Every multiple of an eigenvector is also an eigenvector: $A(2\mathbf{v}) =
2A\mathbf{v} = \lambda(2\mathbf{v})$. So when we talk about an
eigenvector we are really talking about a **direction**; any
representative of it is chosen (usually the simplest one with whole
numbers, or the one of unit length).

## Finding the eigenvalues

Move everything in $A\mathbf{v} = \lambda\mathbf{v}$ to one side. Writing
$\lambda\mathbf{v} = \lambda I\mathbf{v}$:

$$
(A - \lambda I)\mathbf{v} = \mathbf{0}
$$

We want this equation to have a **non-zero** solution. From the previous
sections: $B\mathbf{v} = \mathbf{0}$ has a non-zero solution only if $B$ is
singular, that is $\det B = 0$. So the eigenvalues are the roots of

$$
\det(A - \lambda I) = 0
$$

This is called the **characteristic equation**, and the polynomial in
$\lambda$ on the left the **characteristic polynomial**.

### For 2 × 2

$$
\det \begin{bmatrix} a - \lambda & b \\ c & d - \lambda \end{bmatrix} = (a - \lambda)(d - \lambda) - bc
$$

Expanding:

$$
\lambda^2 - (a + d)\,\lambda + (ad - bc) = 0
$$

$a + d$ is the sum of the diagonal, the **trace**, and $ad - bc$ is the
**determinant**. In short:

$$
\lambda^2 - (\operatorname{tr} A)\,\lambda + \det A = 0
$$

In our example $\operatorname{tr} A = 4$ and $\det A = 3$:

$$
\lambda^2 - 4\lambda + 3 = (\lambda - 3)(\lambda - 1) = 0
$$

The eigenvalues are $\lambda_1 = 3$ and $\lambda_2 = 1$; the same as we
found by trying above.

## Finding the eigenvectors

For each eigenvalue, solve the system $(A - \lambda I)\mathbf{v} =
\mathbf{0}$. The matrix is singular, so there are infinitely many
solutions (a direction); we pick one.

**$\lambda = 3$:**

$$
A - 3I = \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix}
$$

The first row says $-x + y = 0$, so $y = x$. The second row gives the same
information (the rows of a singular matrix are dependent). Choosing $x =
1$ gives $\mathbf{v}_1 = (1, 1)$.

**$\lambda = 1$:**

$$
A - I = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}
$$

$x + y = 0$, so $y = -x$: $\mathbf{v}_2 = (1, -1)$.

**The check is always easy:** multiply the vector you found by $A$ and see
whether $\lambda$ times it comes out.

### A non-symmetric example

$$
B = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}
$$

$\operatorname{tr} B = 7$, $\det B = 12 - 2 = 10$:

$$
\lambda^2 - 7\lambda + 10 = (\lambda - 5)(\lambda - 2) = 0
$$

For $\lambda = 5$, $B - 5I = \begin{bmatrix} -1 & 1 \\ 2 & -2 \end{bmatrix}$:
$y = x$, $\mathbf{v} = (1, 1)$. For $\lambda = 2$, $B - 2I = \begin{bmatrix} 2 & 1 \\ 2 & 1 \end{bmatrix}$:
$2x + y = 0$, $\mathbf{v} = (1, -2)$.

Check: $B(1, -2) = (4 - 2,\ 2 - 6) = (2, -4) = 2 \cdot (1, -2)$ ✓.

## Rules of eigenvalues

An $n \times n$ matrix has $n$ eigenvalues (counting complex ones), and
these rules hold:

| Rule | Written as |
|---|---|
| Sum | $\lambda_1 + \cdots + \lambda_n = \operatorname{tr} A$ |
| Product | $\lambda_1 \cdots \lambda_n = \det A$ |
| Triangular matrix | The eigenvalues are the diagonal entries |
| Powers | The eigenvalues of $A^k$ are $\lambda^k$ (same eigenvectors) |
| Inverse | The eigenvalues of $A^{-1}$ are $1/\lambda$ (same eigenvectors) |
| Shift | The eigenvalues of $A + cI$ are $\lambda + c$ |
| Singular | $\det A = 0 \iff 0$ is an eigenvalue |

With our examples: for $A$, $3 + 1 = 4 = \operatorname{tr} A$ and $3 \cdot
1 = 3 = \det A$. For $B$, $5 + 2 = 7$ and $5 \cdot 2 = 10$. ✓

**The trace and determinant shortcut.** For $2 \times 2$, looking for two
numbers whose sum is the trace and whose product is the determinant is
often quicker than solving the characteristic equation.

**Why is the power rule true?** If $A\mathbf{v} = \lambda\mathbf{v}$, then
$A^2\mathbf{v} = A(\lambda\mathbf{v}) = \lambda A\mathbf{v} =
\lambda^2\mathbf{v}$. Each product adds one more $\lambda$.

### There may be no real eigenvalues

The $90°$ rotation matrix $R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$:
$\operatorname{tr} R = 0$, $\det R = 1$, characteristic equation
$\lambda^2 + 1 = 0$. It has no real solution. Geometrically this makes
perfect sense: a rotation changes the direction of **every** vector;
there is not a single vector whose direction is kept. (With complex
numbers the eigenvalues are $\pm i$; in this course we work with real
eigenvalues.)

## Diagonalisation

If an $n \times n$ matrix $A$ has $n$ independent eigenvectors, we can use
them as a basis. Putting the eigenvectors in the columns of $P$ and the
eigenvalues on the diagonal of a matrix $D$:

$$
A = P D P^{-1}
$$

Why? Each column of $AP$ is $A\mathbf{v}_i = \lambda_i\mathbf{v}_i$, so
$AP = PD$. Multiplying by $P^{-1}$ on the right gives the equality.

**What it means:** applying $A$ splits into three steps:

1. $P^{-1}$: convert the vector to its coordinates in the eigenvector basis,
2. $D$: multiply each coordinate by its own eigenvalue (the simplest transformation),
3. $P$: go back to the standard basis.

In the right basis, $A$ is just a scaling. This is the finest example of
the previous section's idea that choosing the right basis makes a problem
simple.

### Powers become easy

$$
A^k = P D^k P^{-1}
$$

The $P^{-1}P$ in between cancel, and the power of a diagonal matrix is the
power of its diagonal entries. For $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$:

$$
P = \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}
\qquad
D = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}
$$

In practice, splitting the vector into eigenvectors is shorter than
writing $P^{-1}$: $(3, 1) = 2 \cdot (1, 1) + 1 \cdot (1, -1)$. Each piece is
multiplied by its own eigenvalue:

$$
A^5 \begin{bmatrix} 3 \\ 1 \end{bmatrix} = 2 \cdot 3^5 \begin{bmatrix} 1 \\ 1 \end{bmatrix} + 1 \cdot 1^5 \begin{bmatrix} 1 \\ -1 \end{bmatrix} = \begin{bmatrix} 487 \\ 485 \end{bmatrix}
$$

Instead of five matrix multiplications we took powers of two numbers.

## Repeated multiplication and the dominant eigenvector

What happens if we multiply a vector by the same matrix again and again?
Split the vector into eigenvectors: $\mathbf{x} = c_1\mathbf{v}_1 +
c_2\mathbf{v}_2$.

$$
A^k\mathbf{x} = c_1\lambda_1^k\mathbf{v}_1 + c_2\lambda_2^k\mathbf{v}_2
$$

If $|\lambda_1| > |\lambda_2|$, then $\lambda_1^k$ grows much faster and
after a while the second term becomes negligible next to it: the direction
of $A^k\mathbf{x}$ approaches the **dominant eigenvector** ($\mathbf{v}_1$).

<figure class="fig">
<svg viewBox="0 0 350 278" width="350"><line class="line" x1="60" y1="244" x2="60" y2="14"/><line class="grid" x1="290" y1="244" x2="290" y2="14"/><line class="line" x1="60" y1="244" x2="290" y2="244"/><line class="grid" x1="60" y1="14" x2="290" y2="14"/><line class="curve3" stroke-dasharray="4 3" x1="60.0" y1="244.0" x2="290.0" y2="14.0"/><line opacity="0.35" class="curve" x1="60" y1="244" x2="271.3" y2="244.0"/><polygon opacity="0.35" class="dot" points="278.5,244.0 270.3,247.7 270.3,240.3"/><text class="ink" x="284.5" y="258.0" font-size="11" text-anchor="start">x</text><line opacity="0.51" class="curve" x1="60" y1="244" x2="249.0" y2="149.5"/><polygon opacity="0.51" class="dot" points="255.4,146.3 249.7,153.3 246.4,146.7"/><text class="ink" x="261.4" y="150.3" font-size="11" text-anchor="start">Ax</text><line opacity="0.68" class="curve" x1="60" y1="244" x2="225.0" y2="112.0"/><polygon opacity="0.68" class="dot" points="230.6,107.5 226.5,115.5 221.9,109.8"/><text class="ink" x="236.6" y="111.5" font-size="11" text-anchor="start">A²x</text><line opacity="0.84" class="curve" x1="60" y1="244" x2="214.8" y2="100.2"/><polygon opacity="0.84" class="dot" points="220.1,95.3 216.6,103.6 211.6,98.2"/><line opacity="1.00" class="curve" x1="60" y1="244" x2="211.2" y2="96.4"/><polygon opacity="1.00" class="dot" points="216.4,91.4 213.1,99.8 208.0,94.5"/><text class="ink" x="206.4" y="89.4" font-size="11" text-anchor="end">A³x, A⁴x</text><text class="ink" x="175" y="266" font-size="11" text-anchor="middle">The direction approaches the dashed eigenvector line</text></svg>
  <figcaption>Starting from $\mathbf{x} = (1, 0)$ and multiplying again and again by $A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}$, the directions are $0°$, $27°$, $39°$, $43°$, $44°$: they approach the $45°$ direction of the dominant eigenvector $(1, 1)$ (each arrow is scaled to unit length).</figcaption>
</figure>

This is the simplest way to find the eigenvector of the largest
eigenvalue: the **power method**. Start with a random vector, multiply by
$A$, scale it to length 1, repeat.

### What happens in the long run: a Markov chain

In a city the weather is either sunny or rainy each day. The day after a
sunny day is sunny with probability 90%, the day after a rainy day is
sunny with probability 50%. A **transition matrix** describes this (column
= today, row = tomorrow):

$$
M = \begin{bmatrix} 0.9 & 0.5 \\ 0.1 & 0.5 \end{bmatrix}
$$

If today's probabilities are $\mathbf{p}$, tomorrow's are $M\mathbf{p}$
and a week later $M^7\mathbf{p}$. In the long run the probabilities settle
into an **unchanging** $\mathbf{p}$: $M\mathbf{p} = \mathbf{p}$. That is
the eigenvector with eigenvalue $1$!

$$
M - I = \begin{bmatrix} -0.1 & 0.5 \\ 0.1 & -0.5 \end{bmatrix}
$$

$-0.1x + 0.5y = 0$, so $x = 5y$: the eigenvector is $(5, 1)$.
Probabilities must add up to 1; dividing $(5, 1)$ by its sum gives
$\left(\tfrac{5}{6}, \tfrac{1}{6}\right)$. In the long run about 83% of
days are sunny, whatever the weather today.

The other eigenvalue comes from the trace: $0.9 + 0.5 - 1 = 0.4$. Since
$0.4^k$ goes to zero fast, the effect of the starting point fades within
a few weeks.

## Symmetric matrices

The matrices met most often in machine learning are **symmetric**
($A^\mathsf{T} = A$): covariance matrices, $X^\mathsf{T}X$, Hessian
matrices. Symmetric matrices have two lovely properties (the **spectral
theorem**):

1. **All eigenvalues are real.** No "eigenvalue-free" surprises like the
   rotation.
2. **Eigenvectors of different eigenvalues are perpendicular.** In our
   example $(1, 1) \cdot (1, -1) = 0$ ✓.

Scaling the eigenvectors to unit length gives a basis of mutually
perpendicular unit vectors. For the matrix $Q$ of such a basis, $Q^{-1} =
Q^\mathsf{T}$ (taking the transpose is enough to invert it), and

$$
A = Q \Lambda Q^\mathsf{T}
$$

where $\Lambda$ is the diagonal matrix of eigenvalues. A symmetric matrix
does nothing but stretch separately along perpendicular axes.

In the earlier non-symmetric example $B$, the eigenvectors are $(1, 1)$
and $(1, -2)$: their dot product is $1 - 2 = -1 \ne 0$, not perpendicular.

## Eigenvalues in machine learning

**PCA.** The covariance matrix of the data is symmetric. The eigenvector
of its largest eigenvalue is the direction in which the data **spreads
most**; the eigenvalue is the variance in that direction. PCA reduces the
dimension by projecting the data onto the eigenvectors of the few largest
eigenvalues (in detail in the PCA section).

**PageRank.** Think of the web as a Markov chain between pages: a random
surfer clicks one of the links on each page. The long-run share of time
spent on each page is the eigenvector with eigenvalue 1 of the transition
matrix. Google computed this eigenvector with the power method and ranked
pages by it.

**Stability of training.** In gradient descent, how large a step can be is
decided by the largest eigenvalue of the Hessian of the loss. Recurrent
neural networks multiply by the same weight matrix over and over: if the
eigenvalues are above 1 the values explode, below 1 they fade away
("exploding / vanishing gradients").

**Spectral clustering.** The eigenvectors of the matrix of a similarity
graph are used to split data into its natural groups.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\mathbf{v} = \mathbf{0}$ is an eigenvector</p>
      <p>$\det(A - \lambda)$ ($I$ forgotten)</p>
      <p>An eigenvector is unique</p>
      <p>The eigenvalues of $A^k$ are $k\lambda$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>An eigenvector is a non-zero vector</p>
      <p>$\det(A - \lambda I)$: $\lambda$ is subtracted only on the diagonal</p>
      <p>Every multiple of an eigenvector is one too</p>
      <p>The eigenvalues of $A^k$ are $\lambda^k$</p>
    </div>
  </div>
  <figcaption>An eigenvector is a direction; the eigenvalue is the stretch factor along it.</figcaption>
</figure>

- **Subtracting $\lambda$ from every entry.** In $A - \lambda I$, $\lambda$
  is subtracted only from the diagonal entries.
- **Expecting a single solution when finding an eigenvector.** $(A -
  \lambda I)$ is singular; infinitely many solutions come out and you pick
  one. If only $\mathbf{0}$ comes out, the eigenvalue was computed wrong.
- **Skipping the check.** Compute $A\mathbf{v}$ and see whether it equals
  $\lambda\mathbf{v}$; one product is enough.

## Summary

- $A\mathbf{v} = \lambda\mathbf{v}$, $\mathbf{v} \ne \mathbf{0}$: an eigenvector keeps its direction and stretches by the eigenvalue.
- Eigenvalues: $\det(A - \lambda I) = 0$. $2 \times 2$: $\lambda^2 - (\operatorname{tr} A)\lambda + \det A = 0$.
- Eigenvectors: for each $\lambda$ solve $(A - \lambda I)\mathbf{v} = \mathbf{0}$; every multiple is also an eigenvector.
- $\sum \lambda_i = \operatorname{tr} A$, $\prod \lambda_i = \det A$; triangular: the diagonal; $A^k \to \lambda^k$, $A^{-1} \to 1/\lambda$.
- A rotation has no real eigenvalues.
- Diagonalisation: $A = PDP^{-1}$, $A^k = PD^kP^{-1}$.
- Repeated multiplication approaches the dominant eigenvector (power method); the long run of a Markov chain is the eigenvector with eigenvalue 1.
- Symmetric matrix: real eigenvalues, perpendicular eigenvectors, $A = Q\Lambda Q^\mathsf{T}$.
- ML: PCA, PageRank, stability of training, spectral clustering.
