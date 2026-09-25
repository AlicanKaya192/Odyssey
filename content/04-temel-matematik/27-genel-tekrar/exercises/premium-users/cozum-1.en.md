**What is asked?** "At least one" and "exactly one" in independent trials; "at least one" in a choice without replacement from a finite group.

**Idea:** Use the complement for "at least one"; independent probabilities multiply; count choices without replacement with combinations.

**Step 1 — At least one.** No premium: $0.7^3 = 0.343$. $1 - 0.343 = 0.657$.

**Step 2 — Exactly one.** For one ordering $0.3 \cdot 0.7 \cdot 0.7 = 0.147$; the premium user can be any of the $3$: $3 \cdot 0.147 = 0.441$.

**Step 3 — Without replacement.** Choices with no premium $\binom{7}{3} = 35$, all choices $\binom{10}{3} = 120$:

$$
1 - \frac{35}{120} = \frac{85}{120} = \frac{17}{24} \approx 0.708
$$

**Check:** Exactly $0$, $1$, $2$, $3$ premium: $0.343 + 0.441 + 0.189 + 0.027 = 1$ ✓.

**Watch out:** Forgetting the factor $3$ in the second question counts only the ordering "the first is premium, the others are not".

**Answer:** $0.657$, $0.441$, $\frac{17}{24}$.
