**Idea:** A zero determinant means the two columns lie **on the same line**: one is a multiple of the other. Let us write this geometric condition directly.

**Step 1 — The columns.** Column 1 is $(k, 3)$, column 2 is $(4, k + 1)$.

**Step 2 — The proportion condition.** If two vectors lie on one line their components are proportional: the ratio of column 1's components equals column 2's.

$$
\frac{k}{4} = \frac{3}{k + 1}
$$

**Step 3 — Cross-multiply.**

$$
\begin{aligned}
k(k + 1) &= 12 \\
k^2 + k - 12 &= 0 \\
(k + 4)(k - 3) &= 0
\end{aligned}
$$

The same equation as in the first method; both routes state the same condition in different words.

**Step 4 — Look at the columns for each solution.**

- $k = 3$: the columns are $(3, 3)$ and $(4, 4)$. The second is $\tfrac{4}{3}$ times the first; same direction.
- $k = -4$: the columns are $(-4, 3)$ and $(4, -3)$. The second is $-1$ times the first; same line, opposite direction.

In both cases the unit square is squashed into a segment; the transformation cannot be undone.

**Answer:** $3$ and $-4$.
