**What is asked?** The spam probability of two different e-mails with Naive Bayes.

**Idea:** For each class multiply the prior by the conditional probabilities of the features (conditional independence); divide the scores by their total to turn them into probabilities.

**Step 1 — Both words, spam score.** $0.4 \cdot 0.5 \cdot 0.2 = 0.04$.

**Step 2 — The probability.** The non-spam score is $0.6 \cdot 0.1 \cdot 0.25 = 0.015$.

$$
\frac{0.04}{0.04 + 0.015} = \frac{0.04}{0.055} = \frac{8}{11} \approx 0.727
$$

**Step 3 — Only the second word.** Spam: $0.4 \cdot 0.5 \cdot 0.2 = 0.04$ (the absence of the first is $1 - 0.5$). Not spam: $0.6 \cdot 0.9 \cdot 0.25 = 0.135$. Probability $\frac{0.04}{0.175} = \frac{8}{35} \approx 0.229$.

**Check:** On its own the second word appears **less** often in spam ($0.2 < 0.25$); the absence of the first word also counts against spam. A probability below the prior ($0.4$) makes sense ✓.

**Watch out:** Treating a missing word as "no information" and not multiplying; in this form of Naive Bayes absence is evidence too.

**Answer:** $0.04$, $\frac{8}{11}$, $\frac{8}{35}$.
