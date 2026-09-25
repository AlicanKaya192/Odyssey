**What is asked?** Shares of explained variance and the number of components needed for a threshold.

**Idea:** Share $\frac{\lambda_j}{\sum\lambda}$; keep adding until the cumulative share passes the threshold.

**Step 1 — First share.** $\frac{6}{10} = 0.6$.

**Step 2 — First two.** $\frac{6 + 2.5}{10} = 0.85$.

**Step 3 — 95 percent.** Three components give $0.93$, four give $0.97$: at least $4$.

**Check:** All the shares add up to $0.6 + 0.25 + 0.08 + 0.04 + 0.03 = 1$ ✓.

**Watch out:** Choosing the one "closest" to $95$ percent ($0.93$); the question says "at least 95 percent", so the threshold must be passed.

**Answer:** $0.6$, $0.85$, $4$.
