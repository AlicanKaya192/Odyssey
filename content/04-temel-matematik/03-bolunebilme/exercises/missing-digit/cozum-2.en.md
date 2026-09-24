**Idea:** Behind the digit-sum rule is this: a number's remainder on division by $9$ (and $3$) equals its digit sum's remainder. Find the missing digit as "the number that brings the remainder up to zero".

**Step 1 — The remainder of the known digits (mod $9$).** $4 + 8 = 12 = 9 \cdot 1 + 3$: remainder $3$.

**Step 2 — Complete it.** For the total remainder to be $0$, the remainder of $a$ must be $9 - 3 = 6$. The only digit from $0$ to $9$ with remainder $6$ on division by $9$ is $6$.

**Step 3 — The remainder of the known digits (mod $3$).** $5 + 2 = 7 = 3 \cdot 2 + 1$: remainder $1$.

**Step 4 — Complete it.** For the total remainder to be $0$, $b$ must leave remainder $3 - 1 = 2$ on division by $3$. The digits from $0$ to $9$ with remainder $2$ are $2, 5, 8$: exactly $3$ of them.

**Why the same result?** Remainders add: the remainder of a sum is the remainder of the sum of the remainders. The first method set the whole sum equal to a multiple of $9$ or $3$; this one worked with remainders only. Both write the same condition.

**Answer:** $6$ and $3$.
