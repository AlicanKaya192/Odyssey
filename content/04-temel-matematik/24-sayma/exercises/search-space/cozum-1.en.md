**What is asked?** The size of a hyperparameter search and of a feature selection.

**Idea:** Independent settings multiply. Feature subsets are unordered choices; all subsets number $2^n$.

**Step 1 — The grid.** $5 \cdot 4 \cdot 3 = 60$ settings, each trained $5$ times: $300$.

**Step 2 — Exactly $3$ features.** $\binom{10}{3} = \frac{10 \cdot 9 \cdot 8}{6} = 120$.

**Step 3 — Non-empty.** $2^{10} - 1 = 1023$.

**Check:** Subsets with exactly $3$ features must be a small part of all subsets: $120 < 1023$ ✓.

**Watch out:** Order does not matter in a feature subset: $\{x_1, x_2, x_3\}$ and $\{x_3, x_1, x_2\}$ are the same model. $P(10, 3) = 720$ counts each subset $6$ times.

**Answer:** $300$, $120$, $1023$.
