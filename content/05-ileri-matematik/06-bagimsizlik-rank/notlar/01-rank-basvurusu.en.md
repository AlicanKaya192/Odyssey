The short version of everything in the lesson. Come back here when you get stuck on a question.

## Concepts

| Concept | Meaning |
|---|---|
| Linear combination | $c_1\mathbf{v}_1 + \cdots + c_k\mathbf{v}_k$ |
| Span | The set of all linear combinations |
| Dependent | One is a combination of the others; $\sum c_i \mathbf{v}_i = \mathbf{0}$ has a non-zero solution |
| Independent | The only solution of $\sum c_i \mathbf{v}_i = \mathbf{0}$ is $\mathbf{c} = \mathbf{0}$ |
| Basis | An independent group that spans the space |
| Dimension | The number of vectors in a basis |
| Coordinates | The coefficients with respect to a basis (unique) |
| Column space | The span of $A$'s columns = all values of $A\mathbf{x}$ |
| Null space | The solutions of $A\mathbf{x} = \mathbf{0}$ |
| Rank | Number of independent columns = number of pivots = number of independent rows |

## Tests for independence

| Situation | Test |
|---|---|
| Two vectors | Is one a multiple of the other? If so, dependent |
| $n$ vectors in $n$ dimensions | independent if $\det \ne 0$ |
| General | Make them columns, eliminate; independent if every column has a pivot |
| More than $n$ vectors in $n$ dimensions | always dependent |
| A group containing the zero vector | always dependent |

## Rank

- $\operatorname{rank} A \le \min(m, n)$; if equal, **full rank**.
- $\operatorname{rank} A = \operatorname{rank} A^\mathsf{T}$.
- Row operations do not change the rank.

**Rank–nullity:** $\operatorname{rank} A + \dim(\text{null space}) = n$ (number of columns).

## Systems and rank

| Case | Condition |
|---|---|
| A solution exists | $\operatorname{rank} A = \operatorname{rank}\,[A \mid \mathbf{b}]$ |
| Exactly one | also $\operatorname{rank} A = n$ |
| Infinitely many | also $\operatorname{rank} A < n$; solutions = one solution + null space |

## The invertible matrix theorem (n × n)

All equivalent: $A$ invertible $\iff$ $\det A \ne 0$ $\iff$ $\operatorname{rank} A = n$ $\iff$ independent columns $\iff$ null space $= \{\mathbf{0}\}$ $\iff$ exactly one solution for every $\mathbf{b}$.

## Coordinates in another basis

If the basis vectors are the columns of $B$, the coordinates $\mathbf{c}$ of $\mathbf{x}$ satisfy:

$$
B\mathbf{c} = \mathbf{x} \quad \Rightarrow \quad \mathbf{c} = B^{-1}\mathbf{x}
$$

## Practical tips

- A dependence may not be visible; three vectors being pairwise non-parallel is not enough.
- For the rank, eliminate and count the pivots.
- Finding the null space: in echelon form give the free variables values $s, t, \dots$; the coefficient vector of each is a basis vector of the null space.
- Working with rows instead of columns gives the same rank; use whichever is easier.
