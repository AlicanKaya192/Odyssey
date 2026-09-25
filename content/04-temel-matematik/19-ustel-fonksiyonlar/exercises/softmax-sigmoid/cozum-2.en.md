**Idea:** It is no coincidence that the first two answers agree. Dividing the numerator and denominator of softmax by $e^{z_1}$ reveals the sigmoid.

**Step 1 — Divide.**

$$
\begin{aligned}
p_1 &= \frac{e^{z_1}}{e^{z_1} + e^{z_2}} = \frac{1}{1 + \frac{e^{z_2}}{e^{z_1}}} \\
&= \frac{1}{1 + e^{-(z_1 - z_2)}} = \sigma(z_1 - z_2)
\end{aligned}
$$

**Step 2 — The numbers.** $\frac{e^{z_2}}{e^{z_1}} = \frac{1}{3}$, so both questions give $\frac{1}{1 + 1/3} = \frac{3}{4}$.

**Step 3 — Three classes.** There is no sigmoid shortcut here; the denominator is $12 + 4 + 4 = 20$ and $p_1 = \frac{3}{5}$.

**Why the same result?** With two classes only the **difference** of the scores matters: adding the same number to $z_1$ and $z_2$ multiplies both $e^{z}$'s by the same factor and leaves the ratio unchanged. That is why logistic regression (the sigmoid) is exactly two-class softmax.

**Answer:** $\frac{3}{4}$, $\frac{3}{4}$ and $\frac{3}{5}$.
