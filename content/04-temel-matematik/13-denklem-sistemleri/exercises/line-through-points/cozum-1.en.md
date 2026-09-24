**What is asked?** Finding a model's two parameters from two data points, then using the model.

**Idea:** If the model passes through a point, putting in that point's $x$ must give its $y$. Each point is an equation in $w$ and $b$; two points, two unknowns.

**Step 1 — The equations.**

$$
\begin{cases}
2w + b = 7 \\
5w + b = 16
\end{cases}
$$

**Step 2 — Subtract.** The coefficients of $b$ are the same:

$$
3w = 9 \quad\Rightarrow\quad w = 3
$$

**Step 3 — $b$.** $2 \cdot 3 + b = 7$, $b = 1$. The model is $\hat{y} = 3x + 1$.

**Step 4 — The prediction.** $\hat{y} = 3 \cdot 10 + 1 = 31$.

**Check:** $3 \cdot 2 + 1 = 7$ ✓, $3 \cdot 5 + 1 = 16$ ✓.

**Reading the result:** $w = 3$ means "when $x$ goes up by one, the prediction goes up by $3$"; $b = 1$ is the prediction at $x = 0$. A model built from just two points memorises the data exactly; with many points in real data, regression looks for the line with the smallest error.

**Answer:** $w = 3$, $b = 1$; the prediction is $31$.
