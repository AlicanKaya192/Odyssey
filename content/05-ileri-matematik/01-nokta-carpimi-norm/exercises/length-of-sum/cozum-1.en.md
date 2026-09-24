**What is asked?** We do not know the vectors themselves, only their lengths and their dot product. From these we find the lengths of the sum and the difference.

**Idea:** A vector's dot product with itself is its length squared:

$$
\mathbf{v} \cdot \mathbf{v} = \|\mathbf{v}\|^2
$$

If we multiply $\mathbf{a} + \mathbf{b}$ by itself and expand the brackets as with numbers, only the three things we know come out: $\|\mathbf{a}\|^2$, $\|\mathbf{b}\|^2$ and $\mathbf{a} \cdot \mathbf{b}$.

**Step 1 — Expand the square of the sum's length.** The dot product distributes like multiplication, and since $\mathbf{a} \cdot \mathbf{b} = \mathbf{b} \cdot \mathbf{a}$ the two middle terms combine (just like $(x + y)^2 = x^2 + 2xy + y^2$):

$$
\begin{aligned}
\|\mathbf{a} + \mathbf{b}\|^2 &= (\mathbf{a} + \mathbf{b}) \cdot (\mathbf{a} + \mathbf{b}) \\
&= \mathbf{a} \cdot \mathbf{a} + 2\,\mathbf{a} \cdot \mathbf{b} + \mathbf{b} \cdot \mathbf{b} \\
&= \|\mathbf{a}\|^2 + 2\,\mathbf{a} \cdot \mathbf{b} + \|\mathbf{b}\|^2
\end{aligned}
$$

**Step 2 — Put in the numbers.** $\|\mathbf{a}\|^2 = 9$, $\|\mathbf{b}\|^2 = 25$, $2\,\mathbf{a} \cdot \mathbf{b} = 12$:

$$
\begin{aligned}
\|\mathbf{a} + \mathbf{b}\|^2 &= 9 + 12 + 25 = 46 \\
\|\mathbf{a} + \mathbf{b}\| &= \sqrt{46} \approx 6.78
\end{aligned}
$$

**Step 3 — The difference.** The same expansion; only the middle term turns negative (like $(x - y)^2 = x^2 - 2xy + y^2$):

$$
\begin{aligned}
\|\mathbf{a} - \mathbf{b}\|^2 &= 9 - 12 + 25 = 22 \\
\|\mathbf{a} - \mathbf{b}\| &= \sqrt{22} \approx 4.69
\end{aligned}
$$

**Check (parallelogram law):** Adding the two squares, the middle terms cancel and $2\,(\|\mathbf{a}\|^2 + \|\mathbf{b}\|^2)$ must remain:

$$
46 + 22 = 68 = 2 \cdot (9 + 25)
$$

It holds. ✓

**Watch out:** The most common slip is writing $\|\mathbf{a} + \mathbf{b}\| = 3 + 5 = 8$. Lengths add up only when the two vectors point the same way.

**Answer:** $6.78$ and $4.69$.
