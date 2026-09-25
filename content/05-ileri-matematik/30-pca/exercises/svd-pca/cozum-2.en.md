**Idea:** The share does not depend on scale: it can also be computed from the squared singular values without dividing by $n - 1$.

**Step 1 — Squares.** $s^2 = 400, 100, 25$; total $525$. $\lambda_1 = \frac{400}{10} = 40$.

**Step 2 — $\lambda_3$.** $\frac{25}{10} = 2.5$.

**Step 3 — Share.** $\frac{400}{525} \approx 0.762$.

**Why the same result?** Every eigenvalue carries the same factor $\frac{1}{n - 1}$; it cancels in the ratio. The "explained variance ratio" output of libraries is computed this way.

**Answer:** $40$, $2.5$ and $0.762$.
