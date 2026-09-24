**Idea:** We can also get there without the cosine, using lengths only. Drawing both vectors from the same point, the side joining their tips is $\mathbf{a} - \mathbf{b}$, and we get a triangle. If we know its three sides, we know its angles.

**Step 1 — Two sides: the vectors themselves.**

$$
\begin{aligned}
\|\mathbf{a}\| &= \sqrt{1 + 1 + 0} = \sqrt{2} \\
\|\mathbf{b}\| &= \sqrt{1 + 0 + 1} = \sqrt{2}
\end{aligned}
$$

**Step 2 — The third side: the vector joining the tips.** Find the difference first, then its length:

$$
\begin{aligned}
\mathbf{a} - \mathbf{b} &= (1 - 1,\ 1 - 0,\ 0 - 1) = (0,\ 1,\ -1) \\
\|\mathbf{a} - \mathbf{b}\| &= \sqrt{0 + 1 + 1} = \sqrt{2}
\end{aligned}
$$

**Step 3 — Recognise the triangle.** All three sides are $\sqrt{2}$: this is an **equilateral triangle**. Every angle of an equilateral triangle is $60°$ (three equal angles adding up to $180°$).

The angle between $\mathbf{a}$ and $\mathbf{b}$ is one corner of this triangle, so it is $60°$ too.

**Why the same result?** This is exactly the triangle we used in the lesson to prove the geometric meaning of the dot product. The first method uses that triangle packed into a formula; this one looks at the shape directly.

**Answer:** $60°$.
