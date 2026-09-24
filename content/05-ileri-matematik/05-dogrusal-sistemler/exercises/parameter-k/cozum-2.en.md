**Idea:** Each equation is a line in the plane. The number of solutions depends on how the two lines sit: crossing gives 1, parallel gives 0, coinciding gives infinitely many.

**Step 1 — Compare the slopes.** Solve both equations for $y$:

$$
\begin{aligned}
x + 2y = 3 \;&\Rightarrow\; y = \tfrac{3}{2} - \tfrac{1}{2}x \\
2x + 4y = k \;&\Rightarrow\; y = \tfrac{k}{4} - \tfrac{1}{2}x
\end{aligned}
$$

Both have slope $-\tfrac{1}{2}$: the lines are **always parallel or coinciding**. Crossing, that is a single solution, is impossible.

**Step 2 — When do they coincide?** Two parallel lines are the same line if they cross the $y$-axis at the same place:

$$
\begin{aligned}
\tfrac{k}{4} &= \tfrac{3}{2} \\
k &= 6
\end{aligned}
$$

Put differently: when $k = 6$ the second equation is exactly twice the first, so it repeats the same information.

**Step 3 — $k = 5$.** The intercepts differ ($\tfrac{5}{4} \ne \tfrac{3}{2}$): the lines are parallel and separate. No common point, so $0$ solutions.

**Why the same result?** The left side vanishing entirely in elimination means the two lines have the same slope; the $k - 6$ left on the right is the amount by which the lines are "shifted" apart.

**Answer:** $6$ and $0$.
