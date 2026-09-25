**Idea:** In odds form each feature multiplies by its own likelihood ratio.

**Step 1 — The ratios.** Prior $\frac{0.4}{0.6} = \frac{2}{3}$. First word present: $\frac{0.5}{0.1} = 5$; absent: $\frac{0.5}{0.9} = \frac{5}{9}$. Second word present: $\frac{0.2}{0.25} = 0.8$. The spam score of the two-word e-mail, from the Bayes numerator: $0.04$.

**Step 2 — Both words.** $\frac{2}{3} \cdot 5 \cdot 0.8 = \frac{8}{3}$. Probability $\frac{8/3}{1 + 8/3} = \frac{8}{11}$.

**Step 3 — Only the second.** $\frac{2}{3} \cdot \frac{5}{9} \cdot 0.8 = \frac{8}{27}$. Probability $\frac{8/27}{1 + 8/27} = \frac{8}{35}$.

**Why the same result?** The ratio of the scores $\frac{0.04}{0.015} = \frac{8}{3}$ equals the product of the likelihood ratios; in odds form Naive Bayes combines "how spammy each word is" by multiplication.

**Answer:** $0.04$, $\frac{8}{11}$ and $\frac{8}{35}$.
