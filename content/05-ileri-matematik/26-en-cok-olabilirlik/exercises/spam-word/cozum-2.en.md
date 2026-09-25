**Idea:** The Laplace correction adds two pseudo-emails to each class before the real data: one with the word, one without. Then the plain MLE is taken.

**Step 1 — Without pseudo-observations.** Spam: $0$ times in $40$ emails, proportion $0$.

**Step 2 — Spam.** $1$ time in $42$ emails: $\frac{1}{42} \approx 0.0238$.

**Step 3 — Normal.** $13$ times in $62$ emails: $\frac{13}{62} \approx 0.210$.

**Why the same result?** $\frac{k + 1}{n + 2}$ is the observed proportion after adding $1$ "present" and $1$ "absent" to the data. In Bayesian terms it is the expected value of the posterior under a (uniform) prior that counts every value of $p$ as equally likely; the pseudo-observations are the prior belief dressed as data.

**Answer:** $0$, $0.0238$ and $0.210$.
