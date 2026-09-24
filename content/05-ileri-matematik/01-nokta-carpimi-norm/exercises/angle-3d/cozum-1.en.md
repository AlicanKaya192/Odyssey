**What is asked?** If the two arrows are drawn from the same point, what angle is between them?

**Idea:** The geometric meaning of the dot product gives the angle:

$$
\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\|\,\|\mathbf{b}\|\cos\theta
$$

If we compute the dot product and both lengths from the components, $\cos\theta$ is the only unknown left. From the cosine we get the angle.

**Step 1 — The dot product.** Multiply matching components and add the results:

$$
\begin{aligned}
\mathbf{a} \cdot \mathbf{b} &= 1 \cdot 1 + 1 \cdot 0 + 0 \cdot 1 \\
&= 1 + 0 + 0 = 1
\end{aligned}
$$

**Step 2 — The lengths.** For each vector, add the squared components and take the square root:

$$
\begin{aligned}
\|\mathbf{a}\| &= \sqrt{1^2 + 1^2 + 0^2} = \sqrt{2} \\
\|\mathbf{b}\| &= \sqrt{1^2 + 0^2 + 1^2} = \sqrt{2}
\end{aligned}
$$

**Step 3 — The cosine.** Rearrange the formula for $\cos\theta$ and put the numbers in. $\sqrt{2} \cdot \sqrt{2} = 2$:

$$
\cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|} = \frac{1}{\sqrt{2} \cdot \sqrt{2}} = \frac{1}{2}
$$

**Step 4 — The angle.** The angle whose cosine is $\tfrac{1}{2}$ is $60°$ (from the known angles: $\cos 0° = 1$, $\cos 60° = \tfrac{1}{2}$, $\cos 90° = 0$).

**Reading the result:** The cosine is positive, so the angle is below $90°$: the two vectors face roughly the same side, but not exactly the same direction.

**Answer:** $60°$.
