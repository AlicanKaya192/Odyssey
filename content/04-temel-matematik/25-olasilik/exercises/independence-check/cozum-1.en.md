**What is asked?** The intersection of two events with a known union, a conditional probability, and neither happening.

**Idea:** The union rule used backwards gives the intersection, the definition of conditional probability the second, the complement the third.

**Step 1 — The intersection.** $0.6 + 0.5 - 0.8 = 0.3$.

**Step 2 — Conditional.** $P(A \mid B) = \frac{0.3}{0.5} = 0.6$.

**Step 3 — Neither.** $1 - P(A \cup B) = 0.2$.

**Check:** $P(A \mid B) = 0.6 = P(A)$: knowing $B$ does not change the probability of $A$, so the events are independent. Indeed $0.6 \cdot 0.5 = 0.3$ ✓.

**Watch out:** In $P(A \mid B)$ the denominator is $P(B)$, not $P(A)$; $\frac{0.3}{0.6} = 0.5$ would be $P(B \mid A)$.

**Answer:** $0.3$, $0.6$, $0.2$.
