**What is asked?** Imagine a light shining perpendicular to the line of $\mathbf{b}$: the shadow $\mathbf{a}$ casts on that line. The first question is the shadow's length (a single number), the second is the shadow itself (a vector).

**Idea:** The dot product is $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\cos\theta \cdot \|\mathbf{b}\|$. Here $\|\mathbf{a}\|\cos\theta$ is exactly the shadow's length. So dividing the dot product by $\|\mathbf{b}\|$ leaves the shadow length. The shadow vector is an arrow along $\mathbf{b}$ with that length.

**Step 1 — The pieces we need.**

$$
\begin{aligned}
\mathbf{a} \cdot \mathbf{b} &= 6 \cdot 3 + 2 \cdot 4 = 18 + 8 = 26 \\
\mathbf{b} \cdot \mathbf{b} &= 3^2 + 4^2 = 9 + 16 = 25 \\
\|\mathbf{b}\| &= \sqrt{25} = 5
\end{aligned}
$$

**Step 2 — Scalar projection (the shadow's length).**

$$
\frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{b}\|} = \frac{26}{5} = 5.2
$$

**Step 3 — Vector projection (the shadow itself).** We multiply $\mathbf{b}$ by a number that makes its length $5.2$. That number is $\dfrac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}$: dividing by $\|\mathbf{b}\|$ once gives the length, dividing once more shrinks $\mathbf{b}$ to unit length.

$$
\begin{aligned}
\frac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b} &= \frac{26}{25}\,(3,\ 4) \\
&= (1.04 \cdot 3,\ 1.04 \cdot 4) \\
&= (3.12,\ 4.16)
\end{aligned}
$$

**Check:** If the shadow is right, what is left of $\mathbf{a}$ after removing the shadow must be perpendicular to $\mathbf{b}$:

$$
\begin{aligned}
\mathbf{a} - (3.12,\ 4.16) &= (2.88,\ -2.16) \\
(2.88,\ -2.16) \cdot (3,\ 4) &= 8.64 - 8.64 = 0
\end{aligned}
$$

Perpendicular. ✓ Also the shadow's length is $\sqrt{3.12^2 + 4.16^2} = 5.2$, matching the first answer.

**Watch out:** In the vector projection the denominator is $\mathbf{b} \cdot \mathbf{b} = 25$, not $\|\mathbf{b}\| = 5$. Divide by $5$ and the shadow comes out 5 times too long.

**Answer:** $5.2$ and $(3.12,\ 4.16)$.
