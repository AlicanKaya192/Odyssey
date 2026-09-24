**What is asked?** Expanding a model's squared error as an expression in the learned weight $w$.

**Idea:** $x$ and $y$ are known numbers; the only unknown is $w$. Put in the numbers and expand with the identity for $(a - b)^2$.

**Step 1 — Put in the numbers.**

$$
E(w) = (7 - 2w)^2
$$

**Step 2 — The identity.** $a = 7$, $b = 2w$:

$$
\begin{aligned}
(7 - 2w)^2 &= 7^2 - 2 \cdot 7 \cdot 2w + (2w)^2 \\
&= 49 - 28w + 4w^2
\end{aligned}
$$

**Step 3 — Reorder.** $E(w) = 4w^2 - 28w + 49$.

**Check:** For $w = 3$ directly: $(7 - 6)^2 = 1$. With the expansion: $36 - 84 + 49 = 1$ ✓.

**Reading the result:** The error is a degree-two expression in $w$: its graph is a bowl (a parabola). The $w$ that makes the error smallest is at the bottom of the bowl; for $w = 3.5$, $7 - 7 = 0$ and the error is zero. Training a model means searching for this bottom.

**Watch out:** Writing $(2w)^2 = 2w^2$ is a common slip; the square goes to both the $2$ and the $w$: $4w^2$.

**Answer:** $a = 4$, $b = -28$, $c = 49$.
