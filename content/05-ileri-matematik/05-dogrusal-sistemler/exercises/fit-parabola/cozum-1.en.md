**What is asked?** Finding a model's parameters from data. That is the basic job of machine learning; here the data fit exactly, so solving a linear system is enough.

**Idea:** At each point $x$ is a known number, so $x^2$ is a known coefficient too. The unknowns are $a, b, c$, each to the first power: a **linear** system.

**Step 1 — Write the equations.** For $x = 1, 2, 3$, $a + bx + cx^2 = y$:

$$
\begin{aligned}
a + b + c &= 6 \\
a + 2b + 4c &= 11 \\
a + 3b + 9c &= 18
\end{aligned}
$$

**Step 2 — Augmented matrix and column 1.** $R_2 \to R_2 - R_1$, $R_3 \to R_3 - R_1$:

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & 3 & 5 \\ 0 & 2 & 8 & 12 \end{array}\right]
$$

**Step 3 — Column 2.** $R_3 \to R_3 - 2R_2$: $(0,\ 2 - 2,\ 8 - 6 \mid 12 - 10)$.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & 3 & 5 \\ 0 & 0 & 2 & 2 \end{array}\right]
$$

**Step 4 — Back-substitute.**

$$
\begin{aligned}
2c &= 2 \;\Rightarrow\; c = 1 \\
b + 3c &= 5 \;\Rightarrow\; b = 2 \\
a + b + c &= 6 \;\Rightarrow\; a = 3
\end{aligned}
$$

The model is $\hat{y} = 3 + 2x + x^2$.

**Step 5 — The prediction.**

$$
\hat{y}(4) = 3 + 2 \cdot 4 + 4^2 = 3 + 8 + 16 = 27
$$

**Check:** At the three points: $3 + 2 + 1 = 6$ ✓, $3 + 4 + 4 = 11$ ✓, $3 + 6 + 9 = 18$ ✓.

**Answer:** $a = 3$, $b = 2$, $c = 1$; the prediction is $27$.
