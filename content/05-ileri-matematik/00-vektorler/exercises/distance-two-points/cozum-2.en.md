**Idea:** Once we have the difference vector, there is a shortcut that avoids squares and square roots: multiplying a vector by a number multiplies its length by the same number. We can shrink it to a familiar small vector and scale that length back up.

**Step 1 — The difference vector.** As in the first method, $\overrightarrow{AB} = (6, 8)$.

**Step 2 — Take out the common factor.** Both $6$ and $8$ are divisible by 2:

$$
(6,\ 8) = 2 \cdot (3,\ 4)
$$

**Step 3 — A familiar triangle.** A right triangle with legs 3 and 4 has hypotenuse 5, because $3^2 + 4^2 = 9 + 16 = 25$. Our vector is twice $(3, 4)$, so its length is twice as long too:

$$
\begin{aligned}
\|2 \cdot (3, 4)\| &= 2 \cdot \|(3, 4)\| \\
&= 2 \cdot 5 = 10
\end{aligned}
$$

**Why does this work?** Multiplying every component by $c$ multiplies every square by $c^2$; the square root brings that back down to $|c|$:

$$
\|c\,\mathbf{v}\| = |c| \cdot \|\mathbf{v}\|
$$

**Tip:** Common right-triangle sides: 3-4-5, 5-12-13, 8-15-17. Recognising them speeds up the calculation a lot.

**Answer:** 10.
