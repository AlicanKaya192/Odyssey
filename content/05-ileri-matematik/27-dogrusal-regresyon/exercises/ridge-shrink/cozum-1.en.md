**What is asked?** How the ridge penalty shrinks the coefficient.

**Idea:** $w_\lambda = \frac{\sum xy}{\sum x^2 + \lambda}$.

**Step 1 — Unpenalised.** $\frac{20}{10} = 2$.

**Step 2 — $\lambda = 10$.** $\frac{20}{20} = 1$.

**Step 3 — Target $1.6$.** $\frac{20}{10 + \lambda} = 1.6$, $10 + \lambda = 12.5$, $\lambda = 2.5$.

**Check:** As $\lambda$ grows the denominator grows and $w$ shrinks towards zero: $2 \to 1.6 \to 1$ ✓.

**Watch out:** Adding $\lambda$ to or subtracting it from the numerator; the penalty only increases the coefficient of $w$, that is the denominator.

**Answer:** $2$, $1$, $2.5$.
