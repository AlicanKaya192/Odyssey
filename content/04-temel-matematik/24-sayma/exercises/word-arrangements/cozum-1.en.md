**What is asked?** The numbers of arrangements of a word with distinct letters and a word with repeated letters, and the arrangements with a fixed first letter.

**Idea:** $n$ distinct objects can be arranged in $n!$ orders. If some objects are identical, swapping them gives no new arrangement; divide by those swaps.

**Step 1 — KALEM.** $5$ distinct letters: $5! = 120$.

**Step 2 — BALABAN.** $7$ letters; A $3$ times, B $2$ times, L and N once each:

$$
\frac{7!}{3! \cdot 2!} = \frac{5040}{12} = 420
$$

**Step 3 — Starting with K.** K is in the first place; the remaining $4$ distinct letters in $4! = 24$ orders.

**Check:** Each of the $5$ letters is first equally often: $\frac{120}{5} = 24$ ✓.

**Watch out:** Stopping at $7!$ for BALABAN counts each arrangement $12$ times (the $3!$ swaps of the A's and the $2!$ of the B's).

**Answer:** $120$, $420$, $24$.
