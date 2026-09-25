**Idea:** An outcome not in "$A$ or $B$" is in neither $A$ nor $B$. Finding that is sometimes easier.

**Step 1 — Neither.** Not prime and less than $4$: $\{1\}$. $P = \frac{1}{6}$.

**Step 2 — The union.** $1 - \frac{1}{6} = \frac{5}{6}$.

**Step 3 — Intersection and $A'$.** $P(A \cap B) = P(A) + P(B) - P(A \cup B) = \frac{3}{6} + \frac{3}{6} - \frac{5}{6} = \frac{1}{6}$. $P(A') = 1 - \frac{3}{6} = \frac{1}{2}$.

**Why the same result?** $(A \cup B)' = A' \cap B'$ (De Morgan); the outcomes that are "neither" are exactly those outside the union. Used the other way round, the union rule gives the intersection.

**Answer:** $\frac{5}{6}$, $\frac{1}{6}$ and $\frac{1}{2}$.
