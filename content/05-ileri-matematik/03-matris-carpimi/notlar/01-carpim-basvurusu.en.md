The short version of everything in the lesson. Come back here when you get stuck on a question.

## The size rule

$$
(m \times n)(n \times p) = m \times p
$$

The two inner numbers must match; the two outer numbers give the size of
the result.

| Product | Result | Name |
|---|---|---|
| $(1 \times n)(n \times 1)$ | $1 \times 1$ | dot product $\mathbf{a}^\mathsf{T}\mathbf{b}$ |
| $(m \times n)(n \times 1)$ | $m \times 1$ | matrix–vector product |
| $(n \times 1)(1 \times p)$ | $n \times p$ | outer product $\mathbf{a}\mathbf{b}^\mathsf{T}$ |

## The entry rule

$$
c_{ij} = \sum_{k=1}^{n} a_{ik}\, b_{kj} = (\text{row } i \text{ of } A) \cdot (\text{column } j \text{ of } B)
$$

Column view: column $j$ of $AB$ $= A\mathbf{b}_j$.

## Rules

| Valid | Not valid |
|---|---|
| $(AB)C = A(BC)$ | $AB = BA$ (in general) |
| $A(B + C) = AB + AC$ | $(AB)^\mathsf{T} = A^\mathsf{T}B^\mathsf{T}$ |
| $(A + B)C = AC + BC$ | $(A + B)^2 = A^2 + 2AB + B^2$ |
| $AI = IA = A$ | $A^2$ = squaring the entries |
| $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$ | |

$(A + B)^2 = A^2 + AB + BA + B^2$; since $AB \ne BA$, the two middle terms
do not combine.

## The matrix as a transformation

- $A\mathbf{e}_1$ = column 1, $A\mathbf{e}_2$ = column 2.
- Writing the matrix of a transformation: make the images of $\mathbf{e}_1$ and $\mathbf{e}_2$ the columns.
- $A(B\mathbf{x}) = (AB)\mathbf{x}$: first $B$, then $A$ (right to left).

| Transformation | Matrix | $(x, y) \to$ |
|---|---|---|
| Scaling | $\begin{bmatrix} s_1 & 0 \\ 0 & s_2 \end{bmatrix}$ | $(s_1 x,\ s_2 y)$ |
| $90°$ rotation | $\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$ | $(-y,\ x)$ |
| $180°$ rotation | $\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$ | $(-x,\ -y)$ |
| Rotation by $\theta$ | $\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$ | |
| Reflection in the $x$-axis | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ | $(x,\ -y)$ |
| Reflection in the $y$-axis | $\begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$ | $(-x,\ y)$ |
| Reflection in $y = x$ | $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ | $(y,\ x)$ |
| Horizontal shear | $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ | $(x + ky,\ y)$ |
| Projection onto the $x$-axis | $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ | $(x,\ 0)$ |

Rotations and reflections preserve lengths and angles; scalings and
shears do not. A translation ($\mathbf{x} + \mathbf{t}$) is not linear and
cannot be written as a matrix.

## Practical tips

- Write the sizes before multiplying: $(2 \times 3)(3 \times 2) = 2 \times 2$.
  Draw the empty result table, then fill it in.
- After computing each entry, check once more which row and which column
  you used.
- When asked about the order of transformations, translate the sentence
  from right to left: "first $B$, then $A$" $\Rightarrow AB$.
- To check a result, try the unit vectors: $AB\mathbf{e}_1$ must be
  column 1 of $AB$.
