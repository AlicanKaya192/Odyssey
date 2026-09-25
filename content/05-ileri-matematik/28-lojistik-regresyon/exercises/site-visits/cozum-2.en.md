**Idea:** Start from the odds at $x = 0$ and multiply by $2.014$ per visit; when the odds pass $1$, $p$ passes $0.5$.

**Step 1 — Factor.** The log-odds rise by $0.7$ per step; the odds are multiplied by $e^{0.7} \approx 2.014$.

**Step 2 — Start.** Odds $0.1353$, $p = \frac{0.1353}{1 + 0.1353} \approx 0.119$.

**Step 3 — Multiplying.** $x = 1$: $0.272$; $x = 2$: $0.549$; $x = 3$: $1.105 > 1$. First at $3$.

**Why the same result?** The odds passing $1$ is the same as the log-odds passing $0$; the multiplication steps are the values of $e^{-2 + 0.7x}$ at whole numbers $x$.

**Answer:** $2.014$, $0.119$ and $3$.
