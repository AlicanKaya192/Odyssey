**Idea:** Three throws give $2^3 = 8$ paths; each path's probability is the product along its branches. Add them up by the number of makes.

**Step 1 — Exactly $3$.** The single path MMM: $0.343$.

**Step 2 — Exactly $0$.** The single path XXX: $0.027$.

**Step 3 — At least $1$.** Exactly $1$: MXX, XMX, XXM, each $0.7 \cdot 0.3 \cdot 0.3 = 0.063$, total $0.189$. Exactly $2$: MMX, MXM, XMM, each $0.147$, total $0.441$. At least one: $0.189 + 0.441 + 0.343 = 0.973$.

**Why the same result?** All paths add up to $1$; the only path not in "at least one" is XXX. Adding the cases one by one and taking XXX away from $1$ reach the same number; the second is far shorter.

**Answer:** $0.343$, $0.027$ and $0.973$.
