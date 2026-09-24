**Idea:** Let us think about the same question with a picture. Drawing both vectors from the same point makes a parallelogram: $\mathbf{a} - \mathbf{b}$ is the short diagonal joining the tips, $\mathbf{a} + \mathbf{b}$ is the other diagonal. Knowing the sides and the angle between them, the law of cosines gives the diagonals.

**Step 1 — The cosine of the angle between them.** From the geometric meaning of the dot product:

$$
\cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|} = \frac{6}{3 \cdot 5} = \frac{6}{15} = 0.4
$$

**Step 2 — The difference (short diagonal).** $\mathbf{a}$, $\mathbf{b}$ and $\mathbf{a} - \mathbf{b}$ form a triangle; $\mathbf{a} - \mathbf{b}$ is the side opposite the angle. Law of cosines: $c^2 = x^2 + y^2 - 2xy\cos\theta$.

$$
\begin{aligned}
\|\mathbf{a} - \mathbf{b}\|^2 &= 3^2 + 5^2 - 2 \cdot 3 \cdot 5 \cdot 0.4 \\
&= 9 + 25 - 12 = 22 \\
\|\mathbf{a} - \mathbf{b}\| &= \sqrt{22} \approx 4.69
\end{aligned}
$$

**Step 3 — The sum (long diagonal).** Neighbouring angles of a parallelogram add up to $180°$. The angle opposite the long diagonal is $180° - \theta$, and $\cos(180° - \theta) = -\cos\theta$, so the sign turns to plus:

$$
\begin{aligned}
\|\mathbf{a} + \mathbf{b}\|^2 &= 3^2 + 5^2 + 2 \cdot 3 \cdot 5 \cdot 0.4 \\
&= 9 + 25 + 12 = 46 \\
\|\mathbf{a} + \mathbf{b}\| &= \sqrt{46} \approx 6.78
\end{aligned}
$$

**Why the same numbers?** In the lesson, the geometric form of the dot product came from the law of cosines in the first place. The $2\,\mathbf{a} \cdot \mathbf{b}$ term of the first method is the same thing as $2 \cdot 3 \cdot 5 \cdot \cos\theta$ here.

**Answer:** $6.78$ and $4.69$.
