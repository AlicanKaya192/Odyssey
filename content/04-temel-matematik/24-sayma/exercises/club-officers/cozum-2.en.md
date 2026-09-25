**Idea:** Get the number of delegations from the permutation count, and the delegations with Ayse from the thought "every person appears equally often".

**Step 1 — Roles.** $9$ candidates for chair, $8$ for deputy, $7$ for treasurer: $504$.

**Step 2 — Delegation.** The same three people were counted six times in $504$, once for each of the $3! = 6$ ways to hand out the roles: $504 / 6 = 84$.

**Step 3 — Ayse.** The $84$ delegations have $84 \cdot 3 = 252$ seats in total and the $9$ people are symmetric; each person sits in $\frac{252}{9} = 28$ delegations.

**Why the same result?** The equality $\frac{3}{9} \binom{9}{3} = \binom{8}{2}$ says that "fix one person and choose from the rest" and "share the seats equally" reach the same number.

**Answer:** $504$, $84$ and $28$.
