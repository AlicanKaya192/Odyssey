**Idea:** Pick the likelihoods on a scale: if $P(\text{word} \mid \text{not spam}) = q$, then $P(\text{word} \mid \text{spam}) = 8q$. $q$ cancels in the end.

**Step 1 — Prior odds.** $\frac{1}{4}$.

**Step 2 — The first word.** $\frac{8q \cdot 0.2}{8q \cdot 0.2 + q \cdot 0.8} = \frac{1.6}{1.6 + 0.8} = \frac{2}{3}$.

**Step 3 — The second word.** Prior $\frac{2}{3}$, likelihoods $3r$ and $r$: $\frac{3 \cdot \frac{2}{3}}{3 \cdot \frac{2}{3} + \frac{1}{3}} = \frac{2}{2 + \frac{1}{3}} = \frac{6}{7}$.

**Why the same result?** In Bayes' rule $q$ and $r$ cancel between numerator and denominator; only their ratios remain. The odds form is this cancellation done in advance.

**Answer:** $\frac{1}{4}$, $\frac{2}{3}$ and $\frac{6}{7}$.
