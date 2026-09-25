**What is asked?** A classifier's prediction probability, its accuracy, and the probability that it is right when it says "cat".

**Idea:** Put the numbers in a two-way table; each probability is a cell over the right total.

**Step 1 — The table.**

| true \ predicted | cat | dog | total |
|---|---|---|---|
| cat | $70$ | $10$ | $80$ |
| dog | $20$ | $100$ | $120$ |
| total | $90$ | $110$ | $200$ |

**Step 2 — Saying "cat", and accuracy.** $\frac{90}{200} = 0.45$. The correct ones are on the diagonal: $\frac{70 + 100}{200} = 0.85$.

**Step 3 — If it said "cat".** The denominator is the "cat" column: $\frac{70}{90} = \frac{7}{9} \approx 0.78$.

**Check:** $P(\text{says cat} \mid \text{really cat}) = \frac{70}{80} = 0.875$; this differs from the third answer ✓, because the denominators are different groups.

**Watch out:** The third question is called **precision** in machine learning; $\frac{70}{80}$ is **recall**. Mixing them up is a common mistake.

**Answer:** $0.45$, $0.85$, $\frac{7}{9}$.
