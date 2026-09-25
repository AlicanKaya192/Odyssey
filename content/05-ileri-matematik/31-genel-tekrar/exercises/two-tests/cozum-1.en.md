**What is asked?** Total probability, a posterior, and a sequential update.

**Idea:** $P(H \mid +) = \frac{P(+ \mid H)P(H)}{P(+)}$; the posterior is the next step's prior.

**Step 1 — $P(+)$.** $0.018 + 0.049 = 0.067$.

**Step 2 — Posterior.** $\frac{0.018}{0.067} \approx 0.269$.

**Step 3 — Second test.** Prior $0.269$: numerator $0.269 \cdot 0.9 \approx 0.242$, denominator $0.242 + 0.731 \cdot 0.05 \approx 0.242 + 0.037 = 0.278$. Posterior $\approx 0.869$.

**Check:** One positive test raises the probability from $2$ to $27$ percent, a second to $87$ percent; each piece of evidence pushes the same way ✓.

**Watch out:** Mistaking $P(H \mid +)$ for the test's sensitivity ($0.9$); because the base rate is so small, false positives dominate in number.

**Answer:** $0.067$, $\approx 0.269$, $\approx 0.869$.
