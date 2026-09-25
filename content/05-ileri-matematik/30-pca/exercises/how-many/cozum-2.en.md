**Idea:** When $k$ components are kept, the discarded variance is the sum of the remaining eigenvalues. Keeping $95$ percent means discarding at most $5$ percent (here $0.5$).

**Step 1 — First share.** Discarded $2.5 + 0.8 + 0.4 + 0.3 = 4$; kept $1 - 0.4 = 0.6$.

**Step 2 — First two.** Discarded $1.5$; kept $0.85$.

**Step 3 — Threshold.** $k = 3$: discarded $0.7 > 0.5$. $k = 4$: discarded $0.3 \leq 0.5$. At least $4$.

**Why the same result?** The kept and discarded shares add up to $1$; counting one from the end and the other from the start gives the same threshold. Since the discarded variance is exactly the mean squared reconstruction error, this view directly answers "how much error do I accept".

**Answer:** $0.6$, $0.85$ and $4$.
