**What is asked?** A unit vector is a vector whose length is exactly 1. We want the arrow that points the same way as $\mathbf{v}$ but has length 1.

**Idea:** Dividing a vector by a positive number does not change its direction, it only shrinks it. Dividing an arrow of length 10 by 10 gives length 1. So first find the length, then divide every component by it.

**Step 1 — Find the length.**

$$
\begin{aligned}
\|\mathbf{v}\| &= \sqrt{6^2 + (-8)^2} \\
&= \sqrt{36 + 64} \\
&= \sqrt{100} = 10
\end{aligned}
$$

**Step 2 — Divide every component by the length.**

$$
\begin{aligned}
\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|} &= \left(\frac{6}{10},\ \frac{-8}{10}\right) \\
&= (0.6,\ -0.8)
\end{aligned}
$$

**Check:** Is the length really 1?

$$
\sqrt{0.6^2 + (-0.8)^2} = \sqrt{0.36 + 0.64} = \sqrt{1} = 1
$$

The direction stayed the same too: both components were divided by the same number, so their ratio did not change and the signs stayed put. ✓

**Watch out:** Do not drop the minus sign. $(0.6,\ 0.8)$ is also a unit vector, but it points somewhere else.

**Why is it useful?** A unit vector carries only direction. To compare the directions of two vectors regardless of their lengths (like cosine similarity in the next section), both are turned into unit vectors first.

**Answer:** $(0.6, -0.8)$.
