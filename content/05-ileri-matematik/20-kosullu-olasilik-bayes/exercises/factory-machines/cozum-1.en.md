**What is asked?** The total probability of a defect and the posterior probabilities of which machine a defective product came from.

**Idea:** The machines split the sample space into three pieces. The law of total probability gives $P(\text{defective})$ and Bayes' rule the posteriors.

**Step 1 — The shares.** A: $0.5 \cdot 0.02 = 0.010$; B: $0.3 \cdot 0.03 = 0.009$; C: $0.2 \cdot 0.05 = 0.010$. Total $0.029$.

**Step 2 — C.** $P(C \mid \text{defective}) = \frac{0.010}{0.029} \approx 0.345$.

**Step 3 — B.** $P(B \mid \text{defective}) = \frac{0.009}{0.029} \approx 0.310$.

**Check:** A is also $\frac{0.010}{0.029} \approx 0.345$; the three add up to $0.345 + 0.310 + 0.345 = 1$ ✓.

**Watch out:** Taking C's posterior to be its defect rate ($0.05$) or its production share ($0.2$); the posterior is the share of their product in the total.

**Answer:** $0.029$, $\approx 0.345$, $\approx 0.310$.
