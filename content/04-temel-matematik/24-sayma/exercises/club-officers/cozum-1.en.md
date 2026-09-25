**What is asked?** Ordered and unordered choices of three from the same $9$ people, and the choices that include a given person.

**Idea:** With different roles, who gets which role matters (permutation); with the same role only who is chosen matters (combination).

**Step 1 — Three roles.** $P(9, 3) = 9 \cdot 8 \cdot 7 = 504$.

**Step 2 — The delegation.** $\binom{9}{3} = \frac{504}{3!} = \frac{504}{6} = 84$.

**Step 3 — Delegations with Ayse.** Ayse's place is guaranteed; the other $2$ come from the remaining $8$: $\binom{8}{2} = 28$.

**Check:** Delegations without Ayse: $\binom{8}{3} = 56$; $28 + 56 = 84$ ✓.

**Watch out:** Writing $\binom{9}{2}$ in the third question counts Ayse as choosable again; she is already placed and $8$ people are left.

**Answer:** $504$, $84$, $28$.
