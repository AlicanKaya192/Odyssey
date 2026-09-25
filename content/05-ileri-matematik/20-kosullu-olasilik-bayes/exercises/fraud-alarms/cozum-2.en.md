**Idea:** Multiply the prior odds by the likelihood ratio; read the counts off the probability afterwards.

**Step 1 — The ratios.** Prior odds $\frac{0.002}{0.998} \approx \frac{1}{499}$. Likelihood ratio $\frac{0.95}{0.01} = 95$.

**Step 2 — Posterior.** Odds $\frac{95}{499} \approx 0.190$; probability $\frac{95}{95 + 499} = \frac{95}{594} \approx 0.160$.

**Step 3 — The counts.** The alarm rate is $0.95 \cdot 0.002 + 0.01 \cdot 0.998 = 0.01188$; in $100{,}000$ transactions $1188$ alarms, $0.16$ of which is about $190$.

**Why the same result?** The fraction $\frac{95}{594}$ is $\frac{190}{1188}$ simplified; the odds form gives the same share without choosing a number of transactions.

**Answer:** $1188$, $190$ and $0.160$.
