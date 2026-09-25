**Idea:** Instead of dividing for repeated letters, choose the places each letter goes to among the $7$ places with combinations.

**Step 1 — KALEM.** $5$ places for K, $4$ remaining for A, … $5 \cdot 4 \cdot 3 \cdot 2 \cdot 1 = 120$.

**Step 2 — BALABAN.** The places of the three A's: $\binom{7}{3} = 35$. From the remaining $4$, the places of the two B's: $\binom{4}{2} = 6$. L and N into the last $2$ places: $2$ ways. Total $35 \cdot 6 \cdot 2 = 420$.

**Step 3 — Starting with K.** The first place is reserved for K; A, L, E, M go into the other $4$ places: $4 \cdot 3 \cdot 2 \cdot 1 = 24$.

**Why the same result?** $\binom{7}{3}\binom{4}{2} \cdot 2! = \frac{7!}{3!4!} \cdot \frac{4!}{2!2!} \cdot 2! = \frac{7!}{3!2!}$: choosing places and dividing out overcounting are two ways of writing the same calculation.

**Answer:** $120$, $420$ and $24$.
